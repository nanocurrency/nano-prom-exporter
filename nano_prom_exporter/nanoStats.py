import psutil
import os
from socket import gethostname
from prometheus_client import Info, Gauge, push_to_gateway, ProcessCollector


class nano_nodeProcess:
    def __init__(self, nanoProm):
        self.nanoProm = nanoProm

    def find_procs_by_name(self, name):
        "Return a list of processes matching 'name'."
        ls = []
        for p in psutil.process_iter(attrs=['name', 'pid']):
            if name in p.info['name']:
                ls.append(p)
        return ls

    def node_process_stats(self):
        nano_pid = self.find_procs_by_name('nano_node')
        for a in nano_pid:
            self.get_threads_cpu_percent(a)
            try:
                self.nanoProm.rss.labels(a.pid).set(a.memory_info().rss)
            except Exception as e:
                print(e)
            try:
                self.nanoProm.vms.labels(a.pid).set(a.memory_info().vms)
            except Exception as e:
                print(e)
            try:
                self.nanoProm.pp.labels(a.pid).set(a.memory_info().paged_pool)
            except Exception as e:
                print(e)
            try:
                self.nanoProm.cpu.labels(a.pid).set(a.cpu_percent())
            except Exception as e:
                print(e)

    def get_threads_cpu_percent(self, p, interval=0.1):
        try:
            total_percent = p.cpu_percent(interval)
            total_time = sum(p.cpu_times())
            for t in p.threads():
                self.nanoProm.threads.labels(p.pid, t.id).set(
                    total_percent * ((t.system_time + t.user_time)/total_time))
        except Exception as e:
            print(e)


class nanoProm:
    def __init__(self, config, registry):
        self.config = config
        self.ActiveDifficulty = Gauge('nano_active_difficulty',
                                      'Active Difficulty Multiplier', registry=registry)
        self.threads = Gauge('nano_node_threads', 'Thread %', [
                             'pid', 'tid'], registry=registry)
        self.BlockCount = Gauge(
            'nano_block_count', 'Block Count Statistics', ['type'], registry=registry)
        self.ConfirmationHistory = Gauge(
            'nano_confirmation_history', 'Block Confirmation Average', ['count'], registry=registry
        )
        self.Peers = Gauge(
            'nano_peers', 'Peer Statistics', ['endpoint', 'protocol_version'], registry=registry)
        self.StatsCounters = Gauge(
            'nano_stats_counters', 'Stats Counters', ['type', 'detail', 'dir'], registry=registry)
        self.Uptime = Gauge('nano_uptime', 'Uptime Counter in seconds',
                            registry=registry)
        self.Version = Info(
            'nano_version', 'Nano Version details', registry=registry)
        self.rss = Gauge(
            'nano_node_memory_rss', 'nano_node process memory', ['pid'], registry=registry)
        self.vms = Gauge(
            'nano_node_memory_vms', 'nano_node process memory', ['pid'], registry=registry)
        self.pp = Gauge(
            'nano_node_memory_paged_pool', 'nano_node process memory', ['pid'], registry=registry)
        self.cpu = Gauge('nano_node_cpu_usage', 'nano_node cpu usage', [
                         'pid'], registry=registry)
        self.databaseSize = Gauge(
            'nano_node_database', 'nano_node data', ['type'], registry=registry)
        self.Frontiers = Gauge('nano_node_frontier_count',
                               'local node frontier count', registry=registry)
        self.OnlineStake = Gauge(
            'nano_node_online_stake_total', 'Online Stake Total', registry=registry)
        self.PeersStake = Gauge(
            'nano_node_peers_stake_total', 'Peers Stake Total', registry=registry)

    def update(self, stats):
        try:
            self.ActiveDifficulty.set(stats.ActiveDifficulty)
            self.Uptime.set(stats.Uptime)
            self.Frontiers.set(stats.Frontiers)
            if os.path.exists(self.config.nodeDataPath+"data.ldb"):
                self.databaseSize.labels("lmdb").set(
                    os.path.getsize(self.config.nodeDataPath+"data.ldb"))
            self.OnlineStake.set(stats.OnlineStake)
            self.PeersStake.set(stats.PeersStake)
            for a in stats.BlockCount:
                self.BlockCount.labels(a).set(stats.BlockCount[a])
            for a in stats.Peers['peers']:
                self.Peers.labels(a, stats.Peers['peers'][a])
        except Exception as e:
            print(e)
        try:
            self.ConfirmationHistory.labels(stats.ConfirmationHistory['confirmation_stats']['count']).set(
                stats.ConfirmationHistory['confirmation_stats']['average'])
        except Exception as e:
            print(e)
        try:
            for entry in stats.StatsCounters['entries']:
                self.StatsCounters.labels(
                    entry['type'], entry['detail'], entry['dir']).set(entry['value'])
            self.Version.info({'rpc_version': stats.Version['rpc_version'], 'store_version': stats.Version['store_version'], 'protocol_version': stats.Version['protocol_version'], 'node_vendor': stats.Version['node_vendor'],
                               'store_vendor': stats.Version['store_vendor'], 'network': stats.Version['network'], 'network_identifier': stats.Version['network_identifier'], 'build_info': stats.Version['build_info']})
        except Exception as e:
            print(e)

    def pushStats(self, registry):
        push_to_gateway(self.config.pushGateway,
                        job=gethostname(), registry=registry)

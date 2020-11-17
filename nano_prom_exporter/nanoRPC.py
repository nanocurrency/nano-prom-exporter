import os

import requests


def to_multiplier(difficulty: int, base_difficulty) -> float:
    return float((1 << 64) - base_difficulty) / float((1 << 64) - difficulty)


class nanoStats:
    def __init__(self, collection):
        """Collection of stats to pass into rpc
            ActiveDifficulty
            BlockCount
            ConfirmationHistory
            Peers
            StatsCounters
            StatsObjects
            StatsObjects
            Uptime
            Version
            Frontiers
            OnlineStake
            PeersStake
        """
        self.ActiveDifficulty = collection['active_difficulty']['multiplier']
        self.NetworkReceiveCurrent = to_multiplier(
            int(
                collection['active_difficulty']['network_receive_current'],
                16),
            int(
                collection['active_difficulty']['network_receive_minimum'],
                16))
        self.BlockCount = collection['block_count']
        self.ConfirmationHistory = collection['confirmation_history']
        self.Peers = collection['peers']
        self.StatsCounters = collection['stats_counters']
        try:
            self.StatsObjects = collection['stats_objects']['node']
        except Exception as e:
            print(e.__str__())
            self.StatsObjects = None
        self.Uptime = collection['uptime']['seconds']
        self.Version = collection['version']
        self.Frontiers = collection['frontier_count']['count']
        self.OnlineStake = collection['confirmation_quorum']['online_stake_total']
        self.PeersStake = collection['confirmation_quorum']['peers_stake_total']
        self.TelemetryRaw = collection['telemetry_raw']['metrics']
        self.Telemetry = collection['telemetry']


class nanoRPC:
    def __init__(self, config):
        
        """Helper class for RPC calls
        accepts config returns stats object
        """
        self.uri = "http://" + config.rpc_ip + ":" + config.rpc_port
        self.lastData = {}
        Version = {"action": "version"}
        BlockCount = {"action": "block_count"}
        Peers = {"action": "peers"}
        StatsCounters = {"action": "stats", "type": "counters"}
        StatsObjects = {"action": "stats", "type": "objects"}
        ConfirmationHistory = {"action": "confirmation_history"}
        Uptime = {"action": "uptime"}
        ActiveDifficulty = {"action": "active_difficulty"}
        Frontiers = {"action": "frontier_count"}
        Quorum = {"action": "confirmation_quorum"}
        TelemetryRaw = {"action": "telemetry", "raw": "true"}
        Telemetry = {"action": "telemetry"}
        self.Commands = {
            "version": Version,
            "block_count": BlockCount,
            "peers": Peers,
            "stats_counters": StatsCounters,
            "stats_objects": StatsObjects,
            "confirmation_history": ConfirmationHistory,
            "uptime": Uptime,
            "active_difficulty": ActiveDifficulty,
            "frontier_count": Frontiers,
            "confirmation_quorum": Quorum,
            "telemetry_raw": TelemetryRaw,
            "telemetry": Telemetry}

    def rpcWrapper(self, msg):
        try:
            connection = requests.post(url=self.uri, json=msg)
        except Exception as e:
            if os.getenv("NANO_PROM_DEBUG"):
                print(e)
            return None
        return connection

    def gatherStats(self, rpcLatency):
        for a in self.Commands:
            try:
                with rpcLatency.labels(a).time():
                    response = self.rpcWrapper(self.Commands[a])
                    response = response.json()
                    self.lastData[a] = response
            except Exception as e:
                if os.getenv("NANO_PROM_DEBUG"):
                    print(e)
        stats = nanoStats(self.lastData)
        return stats

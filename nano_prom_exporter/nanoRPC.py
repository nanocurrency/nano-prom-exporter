import requests
import os


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
        self.BlockCount = collection['block_count']
        self.ConfirmationHistory = collection['confirmation_history']
        self.Peers = collection['peers']
        self.StatsCounters = collection['stats_counters']
        try:
            self.StatsObjects = collection['stats_objects']['node']
        except:
            self.StatsObjects = None
        self.Uptime = collection['uptime']['seconds']
        self.Version = collection['version']
        self.Frontiers = collection['frontier_count']['count']
        self.OnlineStake = collection['confirmation_quorum']['online_stake_total']
        self.PeersStake = collection['confirmation_quorum']['peers_stake_total']


class nanoRPC:
    def __init__(self, config):
        self.uri = "http://"+config.rpcIP+":"+config.rpcPort
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
        self.Commands = {"version": Version, "block_count": BlockCount,
                         "peers": Peers, "stats_counters": StatsCounters,
                         "stats_objects": StatsObjects,
                         "confirmation_history": ConfirmationHistory,
                         "uptime": Uptime, "active_difficulty": ActiveDifficulty,
                         "frontier_count": Frontiers, "confirmation_quorum": Quorum}

    def rpcWrapper(self, msg):
        try:
            connection = requests.post(url=self.uri, json=msg)
        except Exception as e:
            if os.getenv("NANO_PROM_DEBUG"):
                print(e)
            else:
                pass
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
                else:
                    pass
        stats = nanoStats(self.lastData)
        return stats

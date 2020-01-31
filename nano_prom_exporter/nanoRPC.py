import requests


class nanoStats:
    def __init__(self, collection):
        self.ActiveDifficulty = collection['ActiveDifficulty']['multiplier']
        self.BlockCount = collection['BlockCount']
        self.ConfirmationHistory = collection['ConfirmationHistory']
        self.Peers = collection['Peers']
        self.StatsCounters = collection['StatsCounters']
        self.Uptime = collection['Uptime']['seconds']
        self.Version = collection['Version']
        self.Frontiers = collection['Frontiers']['count']
        self.OnlineStake = collection['Quorum']['online_stake_total']
        self.PeersStake = collection['Quorum']['peers_stake_total']


class nanoRPC:
    def __init__(self, config):
        self.uri = "http://"+config.rpcIP+":"+config.rpcPort
        self.lastData = {}
        Version = {"action": "version"}
        BlockCount = {"action": "block_count"}
        Peers = {"action": "peers"}
        StatsCounters = {"action": "stats", "type": "counters"}
        ConfirmationHistory = {"action": "confirmation_history"}
        Uptime = {"action": "uptime"}
        ActiveDifficulty = {"action": "active_difficulty"}
        Frontiers = {"action": "frontier_count"}
        Quorum = {"action": "confirmation_quorum"}
        self.Commands = {"Version": Version, "BlockCount": BlockCount,
                         "Peers": Peers, "StatsCounters": StatsCounters,
                         "ConfirmationHistory": ConfirmationHistory,
                         "Uptime": Uptime, "ActiveDifficulty": ActiveDifficulty,
                         "Frontiers": Frontiers, "Quorum": Quorum}

    def rpcWrapper(self, msg):
        try:
            connection = requests.post(url=self.uri, json=msg)
        except Exception as e:
            print(e)
            return None
        return connection

    def gatherStats(self, rpcLatency):
        try:
            for a in self.Commands:
                with rpcLatency.labels(a).time():
                    response = self.rpcWrapper(self.Commands[a])
                    response = response.json()
                    self.lastData[a] = response
            stats = nanoStats(self.lastData)
            return stats
        except:
            return None

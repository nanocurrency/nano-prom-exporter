class config:
    def __init__(self, args):
        self.rpcIP = args.rpchost
        self.rpcPort = args.rpcport
        self.pushGateway = args.pushgateway
        self.nodeDataPath = args.datapath
        self.hostname = args.hostname
        self.interval = args.interval
        self.username = args.username
        self.password = args.password

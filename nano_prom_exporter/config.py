import configparser


class config:
    def __init__(self, args):
        self.rpcIP = args.rpchost
        self.rpcPort = args.rpcport
        self.pushGateway = {args.pushgateway: {
            "username": args.username, "password": args.password}}
        self.nodeDataPath = args.datapath
        self.hostname = args.hostname
        self.interval = args.interval

        print("loaded config, ", self.__config_file(args.config_path))

    def __config_file(self, config_path):
        if config_path == None:
            return None
        try:
            config = configparser.ConfigParser()
            config.read(config_path)
            self.rpcIP = config.get('DEFAULT', 'rpcIP', fallback=self.rpcIP)
            self.rpcPort = config.get(
                'DEFAULT', 'rpcPort', fallback=self.rpcPort)
            self.nodeDataPath = config.get(
                'DEFAULT', 'nodeDataPath', fallback=self.nodeDataPath)
            self.hostname = config.get(
                'DEFAULT', 'hostname', fallback=self.hostname)
            self.interval = config.get(
                'DEFAULT', 'interval', fallback=self.interval)
            self.pushGateway = {}
            for gateway in config.sections():
                username = config.get(gateway, 'username', fallback="")
                password = config.get(gateway, 'password', fallback="")
                if username != "":
                    if password == "":
                        print("Password Needed if using basic Auth ", gateway)
                        exit(0)
                self.pushGateway[gateway] = {
                    "username": username, "password": password}
            return self
        except Exception as e:
            print(e.__str__())

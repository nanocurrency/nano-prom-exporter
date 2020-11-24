import configparser


class Config(object):
    def __init__(self, args):
        self.rpc_ip = args.rpchost
        self.rpc_port = args.rpc_port
        self.push_gateway = {args.push_gateway: {
            "username": args.username, "password": args.password}}
        self.node_data_path = args.datapath
        self.hostname = args.hostname
        self.interval = args.interval

        print("loaded config, ", self.__config_file(args.config_path))

    def __config_file(self, config_path):
        if config_path is None:
            return None
        try:
            config = configparser.ConfigParser()
            config.read(config_path)
            self.rpc_ip = config.get('DEFAULT', 'rpcIp', fallback=self.rpc_ip)
            self.rpc_port = config.get(
                'DEFAULT', 'rpcPort', fallback=self.rpc_port)
            self.node_data_path = config.get(
                'DEFAULT', 'nodeDataPath', fallback=self.node_data_path)
            self.hostname = config.get(
                'DEFAULT', 'hostname', fallback=self.hostname)
            self.interval = config.get(
                'DEFAULT', 'interval', fallback=self.interval)
            self.push_gateway = {}
            for gateway in config.sections():
                username = config.get(gateway, 'username', fallback="")
                password = config.get(gateway, 'password', fallback="")
                if username != "":
                    if password == "":
                        print("Password Needed if using basic Auth ", gateway)
                        exit(0)
                self.push_gateway[gateway] = {
                    "username": username, "password": password}
            return self
        except Exception as e:
            print(e.__str__())

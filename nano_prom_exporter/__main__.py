import argparse
from .config import config
from .nanoRPC import nanoRPC
from .nanoStats import nanoProm
from prometheus_client import CollectorRegistry, Histogram
from time import sleep

parser = argparse.ArgumentParser(
    prog="nano_prom", description="configuration values")
parser.add_argument("--rpchost", help="\"[::1]\" default\thost string",
                    default="[::1]", action="store")
parser.add_argument("--rpcport", help="\"7076\" default\trpc port",
                    default="7076", action="store")
parser.add_argument("--datapath", help="\"~/Nano\" as default",
                    default="~\\Nano", action="store")
parser.add_argument("--pushgateway", help="\"http://localhost:9091\" prometheus push gateway",
                    default="http://localhost:9091", action="store")

args = parser.parse_args()
cnf = config(args)
registry = CollectorRegistry()
rpcLatency = Histogram('nano_rpc_response', "response time from rpc calls", [
                       'method'], registry=registry)

statsCollection = nanoRPC(cnf)
promCollection = nanoProm(cnf, registry)


def main():
    while True:
        stats = statsCollection.gatherStats(rpcLatency)
        promCollection.update(stats)
        promCollection.pushStats(registry)
        sleep(10)


if __name__ == '__main__':
    main()

"""Nano Prometheus Export to Gateway

This Script allows the user to export specific
nano_node based stats to a prometheus gateway
limiting the amount of attack surface normally
needed for exposing stats like this

This script requires
`promethues_client`
`psutil`
`requests` be installed
"""

import argparse
from socket import gethostname
from time import sleep

from prometheus_client import CollectorRegistry, Histogram

from .config import Config
from .nanoRPC import nanoRPC
from .nanoStats import nano_nodeProcess, nanoProm

parser = argparse.ArgumentParser(
    prog="nano_prom", description="configuration values")
parser.add_argument("--rpchost", help="\"[::1]\" default\thost string",
                    default="[::1]", action="store")
parser.add_argument("--rpc_port", help="\"7076\" default\trpc port",
                    default="7076", action="store")
parser.add_argument("--datapath", help="\"~\\Nano\" as default",
                    default="~\\Nano\\", action="store")
parser.add_argument(
    "--push_gateway",
    help="\"http://localhost:9091\" prometheus push gateway",
    default="http://localhost:9091",
    action="store")
parser.add_argument("--hostname", help="job name to pass to prometheus",
                    default=gethostname(), action="store")
parser.add_argument("--interval", help="interval to sleep",
                    default="10", action="store")
parser.add_argument(
    "--username",
    help="Username for basic auth on push_gateway",
    default="",
    action="store")
parser.add_argument(
    "--password",
    help="Password for basic auth on push_gateway",
    default="",
    action="store")
parser.add_argument(
    "--config_path",
    help="Path to config.ini \nIgnores other CLI arguments",
    default=None,
    action="store")

args = parser.parse_args()
cnf = Config(args)
registry = CollectorRegistry()
rpcLatency = Histogram('nano_rpc_response', "response time from rpc calls", [
                       'method'], registry=registry)

statsCollection = nanoRPC(cnf)
promCollection = nanoProm(cnf, registry)
process_stats = nano_nodeProcess(promCollection)


def main():
    while True:
        stats = statsCollection.gatherStats(rpcLatency)
        process_stats.node_process_stats()
        promCollection.update(stats)
        promCollection.pushStats(registry)
        sleep(int(cnf.interval))


if __name__ == '__main__':
    main()

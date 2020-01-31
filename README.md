# nano-prom

### Usage: 
`nano-prom [-h] [--rpchost RPCHOST] [--rpcport RPCPORT] [--datapath DATAPATH] [--pushgateway PUSHGATEWAY]`

### Requirements:
* python 3.7+ https://www.python.org/downloads/
* prometheus-client `pip3 install prometheus-client`
* requests `pip3 install requests`
* psutil `pip3 install psutil`
* `pip3 install .` from repo root

||Optional Arguments| | |
|---|---|---|---|
|-h, --help| | |show this help message and exit|
|--rpchost|RPCHOST|"[::1]"|default host string|
|--rpcport|RPCPORT|"7076"|default rpc port|
|--datapath|DATAPATH|"~/Nano"|as default|
|--pushgateway|PUSHGATEWAY|"http://localhost:9091"| prometheus push gateway|


### Stats exposed:

|Source|Prometheus Series{tag}|Info|
|---|---|---|
|rpc|nano_rpc_response|histogram of rpc response by action|
| |nano_active_difficulty|Active Difficulty Multiplier|
| |nano_block_count{type}|Block Count Statistics|
| |nano_confirmation_history{count}|Block Confirmation Average{count sample size}|
| |nano_node_frontier_count|Frontier Count|
| |nano_node_online_stake_total|Online Stake Total|
| |nano_node_peers_stake_total|Peered Stake Total|
|   |nano_peers{endpoint, protocol_version}|connected to {who}, running {what}|
| |nano_uptime|node uptime(sec)|
| |nano_version|version string|
| |nano_stats_counters{type, detail, dir} |stats counter entries by type detail and direction |
|system|nano_node_memory_rss{pid}|allocated and in ram|
| |nano_node_cpu_usage{pid}|percentage CPU usage|
| |nano_node_database|size of database(bytes)|
| |nano_node_memory_vms{pid}|all memory used|
| |nano_node_memory_paged_pool{pid}| |

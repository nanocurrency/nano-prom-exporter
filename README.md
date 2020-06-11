# nano-prom

### Requirements:
* python 3.7+ https://www.python.org/downloads/

### Installation:
* `pip3 install nano-prom-exporter`  

### Usage: 
`nano-prom [-h] [--rpchost RPCHOST] [--rpcport RPCPORT] [--datapath DATAPATH] [--pushgateway PUSHGATEWAY] [--hostname JOBNAME] [--interval SEC] [--username USERNAME] [--password PASSWORD]`

||Optional Arguments| | |
|---|---|---|---|
|-h, --help| | |show this help message and exit|
|--rpchost|RPCHOST|"[::1]"|default host string|
|--rpcport|RPCPORT|"7076"|default rpc port|
|--datapath|DATAPATH|"~/Nano/"|as default|
|--pushgateway|PUSHGATEWAY|"http://localhost:9091"| prometheus push gateway, push to multiple with `;` separaton|
|--hostname|JOBNAME|socket.gethostname()| jobname to pass to gateway
|--interval|SEC|"10"|seconds between pushing|
|--username|USERNAME|""|http_basic_auth support username|
|--password|PASSWORD|""|http_basic_auth support password|


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
| |nano_node_peer_count|raw peer count|
| |nano_peers{endpoint, protocol_version}|connected to {who}, running {what}|
| |nano_uptime|node uptime(sec)|
| |nano_version|version string|
| |nano_stats_counters{type, detail, dir} |stats counter entries by type detail and direction |
| |nano_stats_objects_count{l1,l2,l3} |stats object count {l1,l2,l3}|
| |nano_stats_objects_size{l1,l2,l3} |stats object size {l1,l2,l3}|
|system|nano_node_memory_rss{pid}|allocated and in ram|
| |nano_node_cpu_usage{pid}|percentage CPU usage|
| |nano_node_threads{pid,tid}|percentage of total CPU per thread id |
| |nano_node_database|size of database(bytes)|
| |nano_node_volume_free|size of volume hosting `DATAPATH` free|
| |nano_node_volume_used|size of volume hosting `DATAPATH` used|
| |nano_node_volume_total|size of volume hosting `DATAPATH` total|
| |nano_node_memory_vms{pid}|all memory used|
| |nano_node_memory_paged_pool{pid}| |

### Development Requirements:
* prometheus-client `pip3 install prometheus-client`
* requests `pip3 install requests`
* psutil `pip3 install psutil`

### Development Installation using venv:
* `python3 -m venv venv`
* `. /venv/bin/activate`
* `pip install -r requirements.txt`
* `pip3 install -e .` from repo root

### DEBUGGING

Setting `NANO_PROM_DEBUG` to `1` will print exceptions, useful for debugging
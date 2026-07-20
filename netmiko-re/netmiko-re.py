from netmiko import ConnectHandler
import re

devices:dict[str,str] = {
    "R1":"172.31.100.4",
    "R2":"172.31.100.5"
}

def main(hosts:dict[str,str], user:str) -> None:

    for key,value in hosts.items():

        network_device = {
            'device_type': 'cisco_ios',
            'host': value,
            'username': user,
            'secret': 'cisco',
            'use_keys': True,
            'key_file': 'netmiko/.key/id_rsa',
            'disabled_algorithms': {'pubkeys': ['rsa-sha2-256', 'rsa-sha2-512']}
        }

        net_connect = ConnectHandler(**network_device)
        net_connect.enable()
        print("Connected to", key)

        if key == "R1":
            result = net_connect.send_command("sh version")
            print("+--- R1 Uptime. ---+")
        elif key == "R2":
            result = net_connect.send_command("sh version")
            print("+--- R2 Uptime. ---+")

        result = re.findall(r"R.*es", str(result))
        print(*result)
        print()
        net_connect.disconnect()

if __name__ == "__main__":
    main(devices,"PC")

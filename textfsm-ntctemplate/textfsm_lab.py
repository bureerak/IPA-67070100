from netmiko import ConnectHandler, BaseConnection

DEVICES:dict[str,str] = {
    "S1":"172.31.100.3",
    "R1":"172.31.100.4",
    "R2":"172.31.100.5"
}

def main(devices:dict[str,str], user:str) -> None :

    for host, ip in devices.items() :

        CONNECT_DATA = {
            'device_type': 'cisco_ios',
            'host': ip,
            'username': user,
            'secret': 'cisco',
            'use_keys': True,
            'key_file': 'netmiko/.key/id_rsa',
            'disabled_algorithms': {'pubkeys': ['rsa-sha2-256', 'rsa-sha2-512']}
        }

        net_connect = ConnectHandler(**CONNECT_DATA)
        net_connect.enable()
        result1 = net_connect.send_command("show cdp neighbor", use_textfsm=True)
        print(*result1, sep="\n")
        
        if host == "S1":
            print("+--- S1 Description. ---+")
            parse_cdp_set_description(result1, host, net_connect)
        elif host == "R1":
            print("+--- R1 Description. ---+")
            parse_cdp_set_description(result1, host, net_connect)
        elif host == "R2":
            print("+--- R2 Description. ---+")
            parse_cdp_set_description(result1, host, net_connect)

        print()
        net_connect.disconnect()

def parse_cdp_set_description(data, host, net_connect:BaseConnection) -> None:

    for d in data:
        neighbor_int = d["platform"] + d["neighbor_interface"]
        local_int = d["local_interface"]
        desc = "Connected to " + neighbor_int + " of " + d["neighbor_name"][:3]

        net_connect.send_config_set([f"int {local_int}", f"description {desc}"])

    if host == "R2":
        net_connect.send_config_set(["int g0/3","description Connected to WAN"])

    elif host == "R1":
        net_connect.send_config_set(["int g0/1","description Connected to PC"])

    elif host == "S1":
        net_connect.send_config_set(["int g0/2","description Connected to PC"])

    return

if __name__ == "__main__":
    main(DEVICES, "PC")
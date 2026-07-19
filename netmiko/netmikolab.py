from netmiko import ConnectHandler

devices:dict[str,str] = {
    "R0":"172.31.100.1",
    "S0":"172.31.100.2",
    "S1":"172.31.100.3",
    "R1":"172.31.100.4",
    "R2":"172.31.100.5"
}

vlan101_setup:list[str] = [
    "conf t",
    "int vlan 101",
    "int g0/1",
    "switchport access vlan 101",
    "int g0/2",
    "switchport access vlan 101",
    "int vlan 101",
    "no shut"
    ]

r1_setup:list[str] = [
    "conf t",
    "int lo0",
    "vrf forwarding control",
    "ip addr 10.0.0.1 255.255.255.255",
    "router ospf 1 vrf control",
    "network 10.0.0.1 0.0.0.0 area 0",
    "network 10.99.1.0 0.0.0.3 area 0",
    "network 10.99.1.4 0.0.0.3 area 0",
    "exit"
    "access-list 20 permit 172.31.100.0 0.0.0.15",
    "access-list 20 permit 10.200.118.0 0.0.0.255",
    "line vty 0 4",
    "access-class 20 in"
]

r2_setup:list[str] = [
    "conf t",
    "int lo0",
    "vrf forwarding control",
    "ip addr 10.0.0.2 255.255.255.255",
    "router ospf 1 vrf control",
    "default-information originate always",
    "network 10.0.0.2 0.0.0.0 area 0",
    "network 10.99.1.4 0.0.0.3 area 0",
    "network 10.99.1.8 0.0.0.3 area 0",
    "exit",
    "int g0/3",
    "ip ospf shutdown",
    "ip nat outside",
    "int range g0/1-2",
    "ip nat inside",
    "exit",
    "access-list 10 permit 10.99.1.0 0.0.0.255",
    "ip nat inside source list 10 interface g0/3 vrf control overload",
    "access-list 20 permit 172.31.100.0 0.0.0.15",
    "access-list 20 permit 10.200.118.0 0.0.0.255",
    "line vty 0 4",
    "access-class 20 in"
]

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

        if key == "S1":
            net_connect.send_config_set(vlan101_setup)
            print("+--- vlan101 Setup. ---+")
        elif key == "R1":
            net_connect.send_config_set(r1_setup)
            print("+--- r1 ospf Setup. ---+")
        elif key == "R2":
            net_connect.send_config_set(r2_setup)
            print("+--- r2 ospf Setup. ---+")

        output = net_connect.send_command("sh ip int br")
        print(output)
        print()
        net_connect.disconnect()

if __name__ == "__main__":

    main(devices,"PC")

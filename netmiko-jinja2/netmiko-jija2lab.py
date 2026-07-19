from netmiko import ConnectHandler
from jinja2 import Environment, FileSystemLoader

def main(hosts:list, user:str) -> None:

    for item in hosts:

        network_device = {
            'device_type': 'cisco_ios',
            'host': item[1],
            'username': user,
            'secret': 'cisco',
            'use_keys': True,
            'key_file': 'netmiko/.key/id_rsa',
            'disabled_algorithms': {'pubkeys': ['rsa-sha2-256', 'rsa-sha2-512']}
        }

        net_connect = ConnectHandler(**network_device)
        net_connect.enable()
        print("Connected to", item[0])

        if item[0] == "S1":
            net_connect.send_config_set(item[2])
            print("+--- vlan101 Setup. ---+")
        elif item[0] == "R1":
            net_connect.send_config_set(item[2])
            print("+--- r1 ospf Setup. ---+")
        elif item[0] == "R2":
            net_connect.send_config_set(item[2])
            print("+--- r2 ospf Setup. ---+")

        #output = net_connect.send_command("sh ip int br")
        #print(output)
        print()
        net_connect.disconnect()

if __name__ == "__main__":

    switch_data = {
        "vlan":"101",
        "interface": ["g0/1","g0/2"]
    }

    router1_data = {
        "loopback": "10.0.0.1",
        "edge": False,
        "networks": {
            "10.99.1.0":"0.0.0.3",
            "10.99.1.4":"0.0.0.3",
            },
        "permits": {
            "172.31.100.0":"0.0.0.15",
            "10.200.118.0":"0.0.0.255" # PC network
        }
    }

    router2_data = {
        "loopback": "10.0.0.2",
        "edge": True,
        "networks": {
            "10.99.1.4":"0.0.0.3",
            "10.99.1.8":"0.0.0.3",
        },
        "permits": {
            "172.31.100.0":"0.0.0.15",
            "10.200.118.0":"0.0.0.255" # PC network
        },
        "outside":"g0/3",
        "insides": ["g0/1","g0/2"],
        "allowed_net":"10.99.1.0",
        "allowed_mask":"0.0.0.255",
    }

    file_loader = FileSystemLoader('./netmiko-jinja2/templates')
    env = Environment(loader=file_loader)

    template = env.get_template('switch-template.j2')
    s1 = template.render(switch_data).splitlines()
    s1 = [comm for comm in s1 if comm]

    template = env.get_template('router-template.j2')
    r1 = template.render(router1_data).splitlines()
    r1 = [comm for comm in r1 if comm]

    r2 = template.render(router2_data).splitlines()
    r2 = [comm for comm in r2 if comm]
    
    devices = [
    ["R0","172.31.100.1",None],
    ["S0","172.31.100.2",None],
    ["S1","172.31.100.3",s1],
    ["R1","172.31.100.4",r1],
    ["R2","172.31.100.5",r2]
    ]

    main(devices,"PC")

import pytest
from netmiko import ConnectHandler, BaseConnection
from textfsm_lab import parse_cdp_set_description

DEVICES:dict[str,str] = {
    "S1":"172.31.100.3",
    "R1":"172.31.100.4",
    "R2":"172.31.100.5"
}

EXPECTED_DATA_S1 = {
        "Gi0/0":"Connected to Gig0/3 of S0.",
        "Gi0/1":"Connected to Gig0/2 of R2.",
        "Gi0/2":"Connected to PC"
    }

EXPECTED_DATA_R1 = {
        "Gi0/0":"Connected to Gig0/1 of S0.",
        "Gi0/1":"Connected to PC",
        "Gi0/2":"Connected to Gig0/1 of R2."
    }

EXPECTED_DATA_R2 = {
        "Gi0/0":"Connected to Gig0/2 of S0.",
        "Gi0/1":"Connected to Gig0/2 of R1.",
        "Gi0/2":"Connected to Gig0/1 of S1."
    }

def connect_device(ip:str, username:str) -> BaseConnection :

    CONNECT_DATA = {
        'device_type': 'cisco_ios',
        'host': ip,
        'username': username,
        'secret': 'cisco',
        'use_keys': True,
        'key_file': 'netmiko/.key/id_rsa',
        'disabled_algorithms': {'pubkeys': ['rsa-sha2-256', 'rsa-sha2-512']}
    }

    net_connect = ConnectHandler(**CONNECT_DATA)
    net_connect.enable()

    return net_connect

@pytest.mark.parametrize(
    "hostname, ip, data, username",
    [
        pytest.param(
            "S1",
            DEVICES["S1"],
            EXPECTED_DATA_S1,
            "PC",
            id="S1"
        ),
        pytest.param(
            "R1",
            DEVICES["R1"],
            EXPECTED_DATA_R1,
            "PC",
            id="R1"
        ),
        pytest.param(
            "R2",
            DEVICES["R2"],
            EXPECTED_DATA_R2,
            "PC",
            id="R2"
        ),
    ])
def test_interface_description( hostname:str, ip:str, data:dict[str,str] , username:str ) -> None:

    net_connect = connect_device(ip, username)

    result = net_connect.send_command("show cdp neighbor", use_textfsm=True)
    parse_cdp_set_description(result, hostname, net_connect)

    output = net_connect.send_command("show interface description", use_textfsm=True)
    output = [ x for x in output if x["status"] == 'up' ]  # type: ignore
    actual_data = { data["port"]: data["description"] for data in output } # type: ignore

    for interface, expected_description in data.items():
        assert interface in actual_data, (
            f"Missing expected interface: {interface}"
        )

        assert actual_data[interface] == expected_description, (
            f"Description mismatch on {interface}: "
            f"expected={expected_description!r}, "
            f"actual={actual_data[interface]!r}"
        )

    net_connect.disconnect()
    print("+---" + hostname + "Tested ---+")

if __name__ == "__main__" :
    print("run via pytest.")
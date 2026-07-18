import paramiko
import time

def main(device:list["str"], user:str, private_path:str, host:str) -> None:

    ssh = paramiko.SSHClient()
    ssh.load_host_keys(host)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)

    for ip in device:

        ssh.connect(
            ip,
            username=user,
            key_filename=private_path,
        )

        _, stdout, _ = ssh.exec_command('sh ip int br')

        print("From " + ip, end="")
        print(stdout.read().decode() + "\n")

        time.sleep(0.2)
        ssh.close()

if __name__ == "__main__":
    main(["172.31.100.1", "172.31.100.2", "172.31.100.3", "172.31.100.4", "172.31.100.5"],
        "PC",
        "./.key/id_rsa",
        "./.key/host_key"
        )
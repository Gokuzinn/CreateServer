from time import sleep as slp
from subprocess import *
from threading import *
import socket
import sys

if len(sys.argv) < 2:
    print("\033[1;34m[*]\033[0m\tUse: python3 %s [IP:PORTA]"%(sys.argv[0]))
    sys.exit()

host = sys.argv[1].split(":")
ip = host[0]
port = host[1]

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((ip,int(port)))
server.listen()

all_clients = {}

def client_thread(client):
    while True:
        try:
            msg = client.recv(1024).decode()
            for c in all_clients:
                c.send(msg.encode())
        except:
            for c in all_clients:
                if c != client:
                    c.send(f"\033[1;31m[-]\033[0m\tO usuário {nome} saiu do chat!!".encode())
            del all_clients[client]
            client.close()
            break

while True:
    print("\033[1;34m[*]\033[0m\tAguardando conexões de usuários...")
    client, end = server.accept()
    print("\033[1;32m[+]\033[0m\tUm usuário conectou ao chat!!\n")
    nome = client.recv(1024).decode()
    all_clients[client] = nome
    for c in all_clients:
        if c != client:
            c.send(f"\033[1;32m[+]\033[0m\tUsuário {nome} entrou no chat!!".encode())
    thread = Thread(target=client_thread,args=(client,))
    thread.start()

import socket
import sys
from threading import *

clients = set()
clients_lock = Lock()

# map load
with open(f"saves/{sys.argv[1]}.gm") as file:
    map_data = file.read()
def listener(client, address):
    print("Accepted connection from: ", address)
    with clients_lock:
        clients.add(client)
    try:    
        while True:
            data = client.recv(256)
            if not data:
                break
            else:
                with clients_lock:
                    if len(clients) == 1:
                        for c in clients:
                            c.sendall(data)
                    else:
                        for c in clients:
                            if client != c:
                                c.sendall(data)
    finally:
        with clients_lock:
            clients.remove(client)
            client.close()

port = 5000

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1',port))
s.listen(3)
th = []

while True:
    print("Server is listening for connections...")
    client, address = s.accept()
    client.send(map_data.encode())
    th.append(Thread(target=listener, args = (client,address)).start())

s.close()
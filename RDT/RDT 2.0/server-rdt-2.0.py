import socket
from socket import *
import random

#The network bits can cause errors hence send an ACK or NACK to detect errors

def server(port):
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('127.0.0.1', port))
    server_socket.listen(1)  # Listen for incoming connections and can have maximum of 1 queued connection.

    print("Server is waiting for connections...")

    while True:
        connection, client_address = server_socket.accept()
        print(f"Connected to {client_address}")

        while True:
            data = connection.recv(1024).decode()
            
            choice=random.choice([True,False])

            if choice:
                print(f"Recieved : {data}.\nSending ACK")
                connection.send(f'ACK'.encode())
            else:
                print(f"Sending NAK")
                connection.send(f'NAK'.encode())

if __name__ == "__main__":
    local_port = 7890
    server(local_port)

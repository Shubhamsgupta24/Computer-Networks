import socket  
from socket import * 
import time

#The network bits can cause errors hence send an ACK or NACK to detect errors

def client(server_address, server_port):
    client_socket = socket(AF_INET,SOCK_STREAM)
    client_socket.connect((server_address, server_port))
    packet_number = 0

    while True:
        message = f"{packet_number}"
        client_socket.send(message.encode())
        response=client_socket.recv(1024).decode()

        if response=='ACK':
            print(f"ACK recieved for packet {packet_number}.")
            packet_number+=1
        else:
            print(f"NAK recieved for packet {packet_number} .")
        
        time.sleep(5)


if __name__ == "__main__":
    server_address = '127.0.0.1'
    server_port = 7890 
    client(server_address, server_port)

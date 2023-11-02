import socket
from socket import *

#RDT 1.0 - We can assume receiving and sending sides of communication as Finite state machines
def receiver(receiver_host, receiver_port):
    sock = socket(AF_INET,SOCK_DGRAM)
    sock.bind((receiver_host, receiver_port))
    print("Ready to receive !!!")
    while True:
        data, addr = sock.recvfrom(1024)
        if not data:
            break
        print(f"Received: {data.decode()}")

receiver('localhost', 6766)
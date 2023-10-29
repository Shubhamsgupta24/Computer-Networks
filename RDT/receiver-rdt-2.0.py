import socket
from socket import *

#RDT 2.0 - It has checksum to detect bit errors along with ACK and NACK
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
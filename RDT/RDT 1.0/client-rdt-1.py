import socket
from socket import *

#RDT 1.0 - We can assume receiving and sending sides of communication as Finite state machines
def sender(message, receiver_host, receiver_port):
    sock = socket(AF_INET,SOCK_DGRAM)
    for i, segment in enumerate(message):
        sock.sendto(segment.encode(), (receiver_host, receiver_port))
        print(f"Sent: {segment}")
    sock.close()

while True:
    choice = input("Do you want to send data ? (y/n) ")
    if choice == 'y':
        msg = input("Enter the message you want to send : ")
        local_host = '127.0.0.1'
        local_port = 6788
        sender([msg], local_host,local_port)
    elif choice == 'n':
        break

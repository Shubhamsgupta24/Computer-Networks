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
        sender([msg], 'localhost', 6766)
    elif choice == 'n':
        break

import socket
from socket import *
import random
import time

# ACKs and NACKs can be corrupted hence,retransmit it and need sequence numbers

CORRUPT_PACKET_THRESHOLD=0.65

def server(port):
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('127.0.0.1', port))
    server_socket.listen(1)

    print("Server is waiting for connections...")

    expected_rem=0

    while True:
        connection, client_address = server_socket.accept()
        print(f"Connected to {client_address}")

        while True:
            data = connection.recv(1024).decode()

            pkt_seq_number,rem=data.split(':')
            rem=int(rem)

            curr_pkt_corrupt_prob=random.random()
            if curr_pkt_corrupt_prob>CORRUPT_PACKET_THRESHOLD:
                print(f'Sending the ACK packet for packet no {pkt_seq_number}.\n')
                time.sleep(3)
                connection.send('ACK'.encode())
            
            elif rem!=expected_rem:
                print(f'Recieved Packet no {pkt_seq_number}.Expected sequence number : {expected_rem} but recieved sequence number : {rem}.\n')
                time.sleep(3)
                connection.send('ACK'.encode())

            else:
                print(f'Recieved Packet no {pkt_seq_number}.Expected sequence number : {expected_rem} and recieved sequence number : {rem}.\n')
                time.sleep(3)
                connection.send('ACK'.encode())
                expected_rem=(expected_rem+1)%2


if __name__ == "__main__":
    server(1225)

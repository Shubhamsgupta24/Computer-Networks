
import socket
import random
import hashlib

# Server configuration
server_host = '127.0.0.1'
server_port = 12345

def calc_checksum(message):
    hash_obj = hashlib.sha256()
    hash_obj.update(message.encode())
    return hash_obj.hexdigest()

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_host, server_port))

print(f"Server listening on {server_host}:{server_port}")

seq_prev = 1
while True:
    #print("Receiving packet-----------")
    data, client_address = server_socket.recvfrom(1024)
    data = data.decode('utf-8')
    data, rcv_checksum, rcv_seq = data.split(':')
    rcv_seq = int(rcv_seq)

    if random.random() < 0.4:
        if random.random() < 0.5:
            data = "error"
        else:
            print("packet lost")
            continue

    if calc_checksum(data) == rcv_checksum and seq_prev != rcv_seq:
        ack_checksum = calc_checksum("ACK")
        print(f"Message received: {data} with seq no - {rcv_seq}")
        ACK = f"ACK:{ack_checksum}:{rcv_seq}"
        server_socket.sendto(ACK.encode('utf-8'), client_address)
        seq_prev = rcv_seq
    elif calc_checksum(data) != rcv_checksum:
        print("Received corrupted packet... Sending ACK with prev seq no")
        ack_checksum = calc_checksum("ACK")
        ACK = f"ACK:{ack_checksum}:{seq_prev}"
        server_socket.sendto(ACK.encode('utf-8'), client_address)
    elif calc_checksum(data) == rcv_checksum and seq_prev == rcv_seq:
        print(f"Received duplicate message with seq no - {rcv_seq}")
        ack_checksum = calc_checksum("ACK")
        ACK = f"ACK:{ack_checksum}:{rcv_seq}"
        server_socket.sendto(ACK.encode('utf-8'), client_address)
        seq_prev = rcv_seq

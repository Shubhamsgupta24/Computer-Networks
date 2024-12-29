import socket
import random
import hashlib
import time

# Client configuration
server_host = '127.0.0.1'
server_port = 12345
TIMEOUT = 4

def calc_checksum(message):
    hash_obj = hashlib.sha256()
    hash_obj.update(message.encode())
    return hash_obj.hexdigest()

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(TIMEOUT)

seq = 0

while True:
    message = input("Enter your message: ")
    checksum = calc_checksum(message)
    packet = f"{message}:{checksum}:{seq}"

    client_socket.sendto(packet.encode('utf-8'), (server_host, server_port))
    ack_rcv = False
    start_time = time.time()

    while not ack_rcv:
        try:
            data, server_address = client_socket.recvfrom(1024)
            response, rcv_checksum, rcv_seq = data.decode('utf-8').split(':')
            rcv_seq = int(rcv_seq)

            if random.random() < 0.2:
                response = "Error"

            if calc_checksum(response) != rcv_checksum:
                print("Corrupted message received... waiting for timeout!!")
            elif seq != rcv_seq:
                print("Response with wrong seq received... waiting for timeout!!")
            else:
                print(f"ACK received with seq number - {rcv_seq}")
                seq +=1
                ack_rcv = True
        except socket.timeout:
            if time.time() - start_time >= TIMEOUT:
                print("Timeout occurred!! Resending the message...")
                client_socket.sendto(packet.encode('utf-8'), (server_host, server_port))

client_socket.close()



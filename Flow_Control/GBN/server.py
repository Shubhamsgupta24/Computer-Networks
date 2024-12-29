import hashlib
import random
import socket
drop = 0.05
prob = 0.2
PORT = 1230
receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver.bind(('localhost', PORT))

receiver.listen(5)

def calculate_checksum(data):
    hash_obj = hashlib.sha256()
    hash_obj.update(data.encode())
    return hash_obj.hexdigest()


def receive_packet(receiver_socket):
    message = receiver_socket.recv(1024)
    return message

def main():
    receiver_socket, addr = receiver.accept()
    answer = ""  
    expected_seq = 0
    while True:

        message = receive_packet(receiver_socket)
        if message[0:4] == b"done":
            print("Complete Message: {}".format(answer))  
            answer = b""
            expected_seq = 0
            break
        elif random.random() < drop:
            print("Simulating an ACK loss event")
            continue
        else:

            seq,message, recv_checksum = message.decode().split(':')
            seq=int(seq)
            check = (calculate_checksum(message)==recv_checksum)
            rand = random.random()
            err = b"ERR"

            if check and seq == expected_seq:
                answer += message  
                print("packet received from client: {}".format(message))
                if rand < prob:
                    print("Sending Corrupted ACK")
                    receiver_socket.send(err)
                else:
                    ack = b"ACK"
                    receiver_socket.send(ack + str(expected_seq).encode('utf-8'))
                    print(f"Sending ACK with sequence: {expected_seq}")
                expected_seq = (expected_seq + 1)
            else:
                if(check==False):
                    print("Corrupted Packet Received")
                else:
                    print(f"Packet of unexpected sequence received. EXPECTED {expected_seq}. RECV: {seq}")
                ack = b"ACK"
                print(f"Sending ACK with sequence: {expected_seq-1}")
                receiver_socket.send(ack + str(expected_seq-1).encode('utf-8'))


main()
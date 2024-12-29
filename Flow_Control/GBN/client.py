import socket
import hashlib
import random
import time
PORT = 1230
server_address = ('localhost', PORT)

def calculate_checksum(data):
    hash_obj = hashlib.sha256()
    hash_obj.update(data.encode())
    return hash_obj.hexdigest()

def Gen_Error(packet):
    prob = 0.2
    rand = random.random()
    if rand < prob:
        return packet+'a'
    else:
        return packet

def send_packet(sender, packet, sequence_number):
    checksum = calculate_checksum(packet)
    packet = Gen_Error(packet)
    msg=f"{sequence_number}:{packet}:{checksum}"
    sender.sendto(msg.encode(),server_address)

def send_window(next_seq_num,base,window_size,packets,sender):
    while next_seq_num < min(base + window_size, len(packets)):
        send_packet(sender, packets[next_seq_num],next_seq_num)
        print(f"Sending packet with sequence number {next_seq_num} and data {packets[next_seq_num]}")
        next_seq_num += 1
        time.sleep(1)
    return next_seq_num
def main():
    sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sender.connect(server_address)
    except ConnectionRefusedError:
        print("Connection refused. Make sure the receiver is running and listening.")
        return
    
    message=input("Enter your message: ")
    if message.lower()== 'exit':
        return
    window_size = 3
    packets = message.split()
    print(f"Packets formed: {packets}")
    base = 0
    next_seq_num = 0
    while base < len(packets):
        print(f"Base: {base}")
        print(f"Next Seq No: {next_seq_num}")
        next_seq_num=send_window(next_seq_num,base,window_size,packets,sender)
        sender.settimeout(5)
        try:
            acknowledgement = sender.recv(1024).decode('utf-8')
            if acknowledgement[0:3] != "ERR":
                if acknowledgement[3] !='-':
                    ack = int(acknowledgement[3])
                    base=ack+1
                else:
                    base=0
                print(f"Acknowledgement received with expected sequence number {acknowledgement[3]}")
        except socket.timeout:
            print(f"Timeout! No Acknowledgement received. Resending packets from sequence number {base} to {next_seq_num-1}.")
            next_seq_num = base
            next_seq_num=send_window(next_seq_num,base,window_size,packets,sender)

    final = "done"
    sender.send(final.encode('utf-8'))
    sender.close()

if __name__ == "__main__":
    main()
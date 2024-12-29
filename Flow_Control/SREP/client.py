import socket
import struct
import random
import select
import time
import threading

ip = '127.0.0.1'
port = 9989

thread_local_curr = threading.local()


def Checksum(packet):
    checksum = 0
    for i in range(0, len(packet), 2):
        data = packet[i:i+2]
        if len(data) == 2:
            value = (ord(data[0]) << 8) + ord(data[1])
            checksum += value
        else:
            value = ord(data)
            checksum += value

    while (checksum >> 16) > 0:
        checksum = (checksum & 0xFFFF) + (checksum >> 16)

    return (~checksum) & 0xFFFF


def Gen_Error(checksum):
    prob = 0.2
    rand = random.random()
    if rand < prob:
        return checksum - 1
    else:
        return checksum


def send(next_seq_num, sender_buffer, sender, packets):
    if not hasattr(thread_local_curr, 'curr'):
        thread_local_curr.curr = next_seq_num
    one = 1
    while thread_local_curr.curr in sender_buffer:
        if (one == 0):
            red_bits = Checksum(packets[thread_local_curr.curr])
            new_bits = Gen_Error(red_bits)
            new_message = str(thread_local_curr.curr).encode(
                'ascii') + packets[thread_local_curr.curr].encode('ascii') + struct.pack('!H', new_bits)
            sender.send(new_message)
            print("Timeout occured, Resending packet with sequence number {} and data {}".format(
                thread_local_curr.curr, packets[thread_local_curr.curr]))
        one = 0
        time.sleep(5)


def main():
    sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender.connect((ip, port))
    message = input("Enter your message (or 'exit' to quit): ")

    if message.lower() == 'exit':
        return 0

    packets = []
    for i in range(0, len(message), 5):
        packets.append(message[i:i+5])

    base = 0
    next_seq_num = 0
    window_size = 4
    curr = 0
    z = 1
    prev = 0
    sender_buffer = []
    while base < len(packets):
        while next_seq_num < min(base + window_size, len(packets)):
            red_bits = Checksum(packets[next_seq_num])
            new_bits = Gen_Error(red_bits)
            new_message = str(next_seq_num).encode(
                'ascii') + packets[next_seq_num].encode('ascii') + struct.pack('!H', new_bits)
            sender.send(new_message)
            print("Sending packet with sequence number {} and data {}".format(
                next_seq_num, packets[next_seq_num]))
            sender_buffer.append(next_seq_num)
            packet_handler = threading.Thread(target=send, args=(
                next_seq_num, sender_buffer, sender, packets))
            next_seq_num += 1
            packet_handler.start()
            time.sleep(1)
        timeout = 1
        to_check = [sender]
        readable, _, _ = select.select(to_check, [], [], timeout)
        if readable:
            acknowledgement = sender.recv(1024).decode('ascii')
            if (acknowledgement[0:3] == "ERR"):
                print("Erroneous message received")
            else:
                ack = int(acknowledgement[3])
                for i in sender_buffer:
                    if (i == ack):
                        sender_buffer.remove(i)
                        if (ack == base):
                            if (len(sender_buffer)):
                                base = min(sender_buffer)
                            else:
                                base = base+4
                        print("Acknowledgement received for {}".format(i))
                        break
    print("done")
    final = "done"
    sender.send(final.encode('ascii'))
    sender.close()


if __name__ == "__main__":
    while True:
        if main() == 0:
            break

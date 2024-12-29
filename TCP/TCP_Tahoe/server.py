import socket
import time
import random

def is_lost(p) :
    return random.random() < p

server_host = "127.0.0.1"  # Replace with the server's IP
server_port = 12345  # Use the same port as the server

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_host, server_port))

cwnd = 1    # Start by sending 1 packet
ssthresh = 4    # Set threshold
count_acks = 0  # Keep count of how many same ACKs arrived
expected_ack = 2    # Expecting next packet

num_packets = int(input("Enter number of packets to send: "))
iter = 1

while (iter <= num_packets) :
    
    count_acks = 0
    isdropped = False
    # If at the last phaseof sending packets...
    if (iter + cwnd > num_packets) :
        send_pkts = list(range(iter, num_packets+1))
    else :
        send_pkts = list(range(iter, iter + cwnd))

    print(f"Congestion window: {send_pkts}\nThreshold: {ssthresh}\n")

    for pkt in send_pkts :

        print(f"Packet {pkt} was sent!")
        time.sleep(1.5)
        if (is_lost(0.35) and not isdropped) :
            # Store dropped packet in separate iterator
            new_iter = pkt
            isdropped = True
            # Signify that packet was dropped
            client_socket.send("-1".encode('utf-8'))
            time.sleep(1)
            ack = client_socket.recv(1024).decode('utf-8')
            count_acks = 1
            continue
        
        message = str(pkt)
        # Wait for ACK
        client_socket.send(message.encode('utf-8'))
        time.sleep(1)
        ack = client_socket.recv(1024).decode('utf-8')
        print(f"Received ACK {ack}")
        
        # print(f"Received ACK {ack}")
        if (int(ack) == expected_ack) :
            expected_ack += 1
            count_acks = 1
        else :
            # print("i was here hehe")
            count_acks += 1
            print(f"count acks; {count_acks}")
       
        if (count_acks >= 3) :
            print("3-duplicate ACKs arrived! Reconfigure congestion window...\n")
            break

    if (count_acks >= 3) :
        print(f"PACKET {new_iter} WAS DROPPED!\n")  
        ssthresh = 1 if (cwnd == 1) else int(cwnd/2)
        cwnd = 1
        iter = new_iter
        continue
    
    # Now if packet was dropped :
    if (isdropped) :
        print(f"PACKET {new_iter} TIMEOUT!\n")
        ssthresh = 1 if (cwnd == 1) else int(cwnd/2)
        cwnd = 1
        iter = new_iter
        continue

    # If smooth sending of packet :
    if (cwnd >= ssthresh) :
        cwnd += 1
    else :
        cwnd = cwnd*2
    iter = send_pkts[-1] + 1
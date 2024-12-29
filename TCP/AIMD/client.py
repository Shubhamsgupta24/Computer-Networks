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

num_packets = int(input("Enter number of packets to send: "))
iter = 1

while (iter <= num_packets) :
    
    isdropped = False
    # If at the last phaseof sending packets...
    if (iter + cwnd > num_packets) :
        send_pkts = list(range(iter, num_packets+1))
    else :
        send_pkts = list(range(iter, iter + cwnd))

    print(f"Congestion window: {send_pkts}\n")

    for pkt in send_pkts :

        print(f"Packet {pkt} was sent!")
        time.sleep(1.5)
        if (is_lost(0.3) and not isdropped) :

            # Store dropped packet in separate iterator
            new_iter = pkt
            isdropped = True
        if (not isdropped) :
            # Send the packet 
            message = str(pkt)
            client_socket.send(message.encode('utf-8'))
    
        # Now if packet was dropped :
    if (isdropped) :
        print(f"PACKET {new_iter} WAS DROPPED!\n")
        cwnd = 1 if (cwnd == 1) else int(cwnd/2)
        iter = new_iter
    # If smooth sending of packet :
    else :
        cwnd += 1
        iter = send_pkts[-1] + 1
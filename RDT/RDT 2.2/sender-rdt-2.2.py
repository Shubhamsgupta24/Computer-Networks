import socket
import struct
import random

ip = input("Enter IP: ")
port = int(input("Enter port number: "))

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
    prob=0.2
    rand=random.random()
    if(rand<prob):
        return checksum-1
    else:
     	return checksum

def main():
    sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender.connect((ip,port))
    message = input("Enter your message (or 'exit' to quit): ")
    if (message.lower() == 'exit'):
        return 0
        
    packets=[]
    for i in range(0,len(message),4):
        packets.append(message[i:i+4])
    i = 0
    seq=0
    while i<len(packets):
        checksumValue=Checksum(packets[i])
        new_bits=Gen_Error(checksumValue)
        new_message = (str(seq%2)).encode('ascii') + (packets[i]).encode('ascii') + struct.pack('!H',new_bits)
        sender.send(new_message)
        print("Sending {}".format(packets[i]))
        acknowledgement = sender.recv(1024).decode('ascii')
        if(acknowledgement[0:4]=="ACK"+str(seq%2)):
            print("Acknowledgement received")
            i+=1
            seq+=1
        else:            
            print("Erroneous message received")
            print("Retransmitting packet")
    final="done"
    sender.send(final.encode('ascii'))
    sender.close()	  

if __name__ == "__main__":
    while True:

        if(main()==0):
            break

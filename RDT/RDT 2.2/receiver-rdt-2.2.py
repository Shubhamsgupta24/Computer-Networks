import struct
import random
import socket

receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver.bind(('127.0.0.1', 1234))
receiver.listen(5)

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
    
def Check_Checksum(message):
	rec = (struct.unpack('!H', message[-2:]))[0]
	actual=Checksum(message[:-2].decode('ascii'))
	if(rec==actual):
		return True
	else:
		return False
	
def main():
		receiver_socket, addr = receiver.accept()	
		answer = ""
		prev_seq=1
		while True:
			message=""
			message = receiver_socket.recv(1024)
			if((message[0:4]) =="done".encode('ascii')):
				print("Complete Message: {}".format(answer))
				answer = ""
				break
			seq=int(message[0:1].decode('ascii'))
			message=message[1:]
			check = Check_Checksum(message)
			message=(message[:-2]).decode('ascii')
			prob=0.5
			rand=random.random()
			err="ERR"
			if(check):
				if prev_seq%2 != seq%2:
					answer+=message
					prev_seq=seq%2
				ack="ACK"
				if(rand<prob):
					print("Erroneous packet received")
					receiver_socket.send(err.encode('ascii'))		
				else:
					print("Current packet received: {}".format(message))
					receiver_socket.send((ack+str(seq%2)).encode('ascii'))
			else:
				ack="ACK"
				receiver_socket.send((ack+str(prev_seq%2)).encode('ascii'))


if __name__ == "__main__":
	while True:
		main()
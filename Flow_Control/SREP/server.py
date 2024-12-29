import struct
import random
import socket

receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver.bind(('127.0.0.1', 9989))
receiver.listen(1)

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
		try:
			answer = [None]*100
			prev_seq=1
			base=0
			window_size=4
			receive_buffer=[0,1,2,3]
			acked=[]
			last=0
			done="done"
			done=done.encode('ascii')
			while True:
				drop=0.3
				message=""
				message = receiver_socket.recv(1024)
				if(message[0:4] == done):
					print("done")
					final_message=""
					for i in range(last+1):
						final_message=final_message+answer[i]
					print("Complete Message: {}".format(final_message))
					answer = [None]*100
					last=0
					break
					
				if random.random()<drop:
					continue
				else:  
					seq=int(message[0:1].decode('ascii'))
					message=message[1:]
					check = Check_Checksum(message)
					message=(message[:-2]).decode('ascii')
					prob=0.5
					rand=random.random()
					err="ERR"
					ack="ACK"
					if(check):
						if(seq in acked):
							receiver_socket.send((ack+str(seq)).encode('ascii'))
						else:
							acked.append(seq)
							for i in receive_buffer:
								if(i==seq):
									last=max(last,i)
									receive_buffer.remove(i)
									print(receive_buffer)
									answer[i]=message
									if(i==base):
										if(len(receive_buffer)==0):
											for i in range(4):
												receive_buffer.append(base+window_size+i)
											base=min(receive_buffer)
										else:
											mini=min(receive_buffer)
											num=mini-base
											for i in range(num):
												receive_buffer.append(base+window_size+i)
											base=mini
									print("Current packet received: {}".format(message))
									receiver_socket.send((ack+str(seq)).encode('ascii'))
									break
		except:
			return 0
if __name__ == "__main__":
	while True:
		if main()==0:
			break

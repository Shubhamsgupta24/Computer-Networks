import threading
import socket
from socket import *

nickname = input("Choose a nickname: ")

client = socket(AF_INET, SOCK_STREAM)   #Creating a TCP Socket
serverName = '127.0.0.1'     #Server name or ip adress of the server
serverPort = 1119     #Port numnber for socket(Change it after then )
client.connect((serverName,serverPort))   #Connecting with the server

def receive():
    while True:
        try:
            message = client.recv(1024).decode("ascii")
            if message == "NICK" :
                client.send(nickname.encode("ascii"))
            else:
                print(message)
        except:
            print("An error occured")
            client.close()
            break

def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode("ascii"))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
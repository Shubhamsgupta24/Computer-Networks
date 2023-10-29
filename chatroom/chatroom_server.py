import threading
import socket
from socket import *

server = socket(AF_INET, SOCK_STREAM)   #Creating a TCP Socket
serverName = '127.0.0.1'     #Server name or ip adress of the server
serverPort = 1119      #Port numnber for socket(Change it after then )
server.bind((serverName,serverPort))        #Binding the server to ip and port number
server.listen()  #Starts listening

clients = []  #Store clients in it
nicknames = []  #Store nicknames of clients in it

def broadcast(message):  #Broadcasting to the chatroom
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} left the chat!".encode("ascii"))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client,addr = server.accept()
        print("Connected with: ",addr)

        client.send("NICK".encode("ascii"))
        nickname = client.recv(1024).decode("ascii")
        nicknames.append(nickname)
        clients.append(client)
        print(f"Nickname of the client is  {nickname} !")
        broadcast(f"{nickname} joined the chat !".encode("ascii"))
        client.send("Connected to the server !".encode("ascii"))

        thread = threading.Thread(target=handle,args=(client,))
        thread.start()

print("Server is Listening....")
receive()
import socket
from socket import *

client_socket = socket(AF_INET, SOCK_STREAM)   #Creating a TCP Socket
serverName = '10.100.102.84'     #Server name or ip adress of the server
serverPort = 12337      #Port numnber for socket(Change it after then )
client_socket.connect((serverName, serverPort))   #Connecting the client to server
payload = input("Enter a message to send to server: ")  #Sending the initial message to server

try:
    while True:
        client_socket.send(payload.encode("utf-8"))
        data = client_socket.recv(1024)   
        print("Message received from server is : ",data.decode("utf-8"))  #Getting the response from server
        more = input("Do you wish to send more data ('y'/'n'): ")
        if more.lower() == 'y':
            payload = input("Enter a message to send to server: ") #Looping the message response loop
        else:
            break
except KeyboardInterrupt:
    print("Exited by user")
client_socket.close()
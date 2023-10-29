import socket
from socket import *

server_socket = socket(AF_INET, SOCK_STREAM)   #Creating a TCP Socket
serverName = '10.100.102.84'     #Server name or ip adress of the server
serverPort = 12337     #Port numnber for socket(Change it after then )
server_socket.bind((serverName,serverPort))        #Binding the server to ip and port number
server_socket.listen(5)   #Listening with a max value of 5 connections in queue

print("The server is ready to receive")
while True:
    client_socket, addr = server_socket.accept()   #Accepting from client: Data + address of client format
    print("Server connected from client adress : ",addr)
    while True:
        data = client_socket.recv(1024)    #Receiving the data and storing it in data variable
        if not data or data.decode("utf-8") == 'END':
            break
        print("Message received from client is : ",data.decode("utf-8"))   #Displaying data from client
        try:
            sentence = input("Enter the message to send to client: ")
            client_socket.send(sentence.encode("utf-8"))     #Sending reply of server to client
        except:
            print("Exited by user")
    client_socket.close()      #Closing client socket
server_socket.close()    #Closing server socket
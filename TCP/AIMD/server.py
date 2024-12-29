import socket

server_host = "127.0.0.1"  # Replace with the server's IP
server_port = 12345  # Use the same port as the server

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_host, server_port))
server_socket.listen(1)

while True:

    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")

    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break
        print(f"Received from client: {data}")

    client_socket.close()
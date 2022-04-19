from socket import *

host = '127.0.0.1'
port = 2121
clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((host,port))
while True:
    command = input('root# ')
    clientSocket.send(command.encode())

    #recv from server
    print(clientSocket.recv(2048).decode())

clientSocket.close()

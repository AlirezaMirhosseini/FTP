from socket import *

host = '127.0.0.1'
port = 25000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind((host,port))
serverSocket.listen(10)
print('now server is ready :)')
while(True):
    privateSocket,address = serverSocket.accept()
    command = privateSocket.recv(2048).decode()
    #some process on data

    #send to client
    privateSocket.close()


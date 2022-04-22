from socket import *
from pyngrok import ngrok

host = '7.tcp.eu.ngrok.io'
port = 14472
downloadCounter = 0
clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((host,port))
CurrentDirectory = '/'
#print('\nHello\n\nWelcome to FTP application\n')
command = 'HELP'
clientSocket.send(command.encode())
print(clientSocket.recv(1024).decode())
while True:
    command = input(f'root:{CurrentDirectory}# ')
    clientSocket.send(command.encode())

    if command[:4] == "DWLD":
            print('Receiving...')
            fileName = command.split()[1]
            print(fileName)            
            data = b""
            is_validate = True
            while True:
                downloadedBin = clientSocket.recv(1024)
                cleared_return = downloadedBin.decode()
                if cleared_return == 'File not accessible':
                    is_validate = False
                    break
                if cleared_return == 'END SEND':
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
            
                print(clientSocket.recv(1024).decode())
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
                wanted = command[3:]
                length = len(wanted)
                if wanted[length-1]=='/':
                    wanted = wanted[:length-1]
                CurrentDirectory = CurrentDirectory + wanted+'/'
        

    else:
        print(clientSocket.recv(1024).decode())

clientSocket.close()

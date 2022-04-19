from socket import *
import os


BASE_DIR = os.getcwd()

def HELP():
    return 'These are available commands\n1.HELP\n2.LIST\n3.DWLD\n4.PWD\n5.CD\n'

def LIST():
    pass

def DWLD(filePath):
    pass

def PWD():
    #os.chdir(BASE_DIR+'/Server')
    real_path = os.getcwd()
    #return real_path[len(BASE_DIR):]
    return real_path

def CD(dirName):
    pass


host = '127.0.0.1'
port = 25000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind((host,port))
serverSocket.listen(10)
print('now server is ready :)')
while(True):
    privateSocket,address = serverSocket.accept()
    command = privateSocket.recv(2048).decode()
    print(f'from client {command} received.')
    command = command.split()
    if command[0] == 'HELP':
        data = HELP()
    elif command[0] == 'LIST':
        data = LIST()    
    elif command[0] == 'PWD':
        data = PWD()
    elif command == 'DWLD':
        data = DWLD(command[1:])
    elif command == 'CD':
        data = CD(command[1:])    
    else:
        data = 'command not found'

    privateSocket.send(data.encode())
    #send to client
    privateSocket.close()


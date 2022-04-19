from posixpath import dirname
from socket import *
import os
import pickle

BASE_DIR = os.getcwd()
CURRENT_PATH = os.getcwd()

def HELP():
    return 'These are available commands\n1.HELP\n2.LIST\n3.DWLD\n4.PWD\n5.CD\n'

def LIST():
    return ''.join(f'{obj}  {str(os.path.getsize(obj))} bits\n' for obj in os.listdir(CURRENT_PATH))

def DWLD(filePath):
    pass

def PWD():
    global BASE_DIR
    real_path = os.getcwd()
    if(BASE_DIR != real_path):
        return real_path[len(BASE_DIR):]
    else:
        return '/'

def CD(dirName):
    dirName = ' '.join(st for st in dirName)
    if dirName[len(dirName)-1] != '/':
        dirName = '/' + dirName
    global CURRENT_PATH,BASE_DIR
    if dirName == '..':
        counter = len(CURRENT_PATH)-1
        while(len(CURRENT_PATH)!=len(BASE_DIR) and CURRENT_PATH[counter]!='/'):
            counter = counter -1
        if CURRENT_PATH[counter] == '/': counter = counter -1
        CURRENT_PATH =  CURRENT_PATH[:counter]    
        return PWD()
            
    else:
        CURRENT_PATH = CURRENT_PATH + dirName
        os.chdir(CURRENT_PATH)
        return PWD()



host = '127.0.0.1'
port = 2121
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind((host,port))
serverSocket.listen(10)
print('now server is ready :)')
privateSocket,address = serverSocket.accept()
while(True):
    command = privateSocket.recv(2048).decode()
    print(f'from client {command} received.')
    command = command.split()
    if command[0] == 'HELP':
        data = HELP()

    elif command[0] == 'LIST':
        data = LIST()    

    elif command[0] == 'PWD':
        data = PWD()

    elif command[0] == 'DWLD':
        data = DWLD(command[1:])

    elif command[0] == 'CD':
        data = CD(command[1:])   
 
    else:
        data = 'command not found'
    privateSocket.send(data.encode())
    #send to client
privateSocket.close()


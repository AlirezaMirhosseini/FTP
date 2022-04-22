from posixpath import dirname
from socket import *
import os
import pickle
from random import randint
import time

BASE_DIR = os.getcwd()
CURRENT_PATH = os.getcwd()

def HELP():
    return 'These are available commands\n1.HELP\n2.LIST\n3.DWLD\n4.PWD\n5.CD\n'

def LIST():
    return ''.join('%-30s'%(obj,) + '%-20s'%(str(os.path.getsize(obj)),) + 'bits\n' for obj in os.listdir(CURRENT_PATH))

def DWLD(fileName):
    global privateSocket
    startDownload = time.time()
    print('Sending...')
    try:
        with open(fileName, "rb") as file:
            data = file.read()
            privateSocket.send(data)
        time.sleep(1)
        privateSocket.send('END SEND'.encode())
        time.sleep(1)
        file_stats = os.stat(fileName)
        print('Done Sending =)')
        timeElapsed = time.time() - startDownload
        return f'   File Size : {file_stats.st_size}\n      Time Elapsed : {timeElapsed} s\n         Closing data TCP connection !\n            Ack sent to TCP control connection !'
    except IOError:
        print("File not accessible")
        return 'File not accessible'
    

def PWD():
    global BASE_DIR,CURRENT_PATH
    if(BASE_DIR != CURRENT_PATH):
        return CURRENT_PATH[len(BASE_DIR):]
    else:
        return '/'

def CD(dirName):
    global CURRENT_PATH,BASE_DIR
    dirName = ' '.join(st for st in dirName)

    if dirName == '..' or dirName == '../':
        counter = len(CURRENT_PATH)-1
        if BASE_DIR == CURRENT_PATH:
              return 'ERROR! YOU DON\'T HAVE PERMISSION TO ACCESS THIS LOACATION\n'
        while(CURRENT_PATH[counter]!='/'):
            counter = counter -1
        CURRENT_PATH =  CURRENT_PATH[:counter]    
        os.chdir(CURRENT_PATH)
        return PWD()
    else:  
        if dirName[len(dirName)-1] == '/':
            dirName = dirName[:len(dirName)-1]
        dirName = '/' + dirName    
        temp = CURRENT_PATH + dirName
        try:
            os.chdir(temp)
            CURRENT_PATH = temp
        except(FileNotFoundError): 
            return f'{dirName[1:]}: No such file or directory'
        return PWD()
    
    

host = '127.0.0.1'
port = 2121
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind((host,port))
serverSocket.listen(10)
print('now server is ready :)')
privateSocket,address = serverSocket.accept()
while(True):
    command = privateSocket.recv(1024).decode()
    print(f'from client {command} received.')
    command = command.split()
    if command[0] == 'HELP':
        data = HELP()

    elif command[0] == 'LIST':
        data = LIST()    

    elif command[0] == 'PWD':
        data = PWD()

    elif command[0] == 'DWLD':
        data = DWLD(command[1])

    elif command[0] == 'CD':
        data = CD(command[1:])   
 
    else:
        data = 'command not found'
    privateSocket.send(data.encode())
    #send to client
privateSocket.close()


import socket
import os
from _thread import *
import traceback
import crypto as Knapsack

ClientMultiSocket = socket.socket()
host = '127.0.0.1'
port = 2004
clientPublicKey = ''

print('Waiting for connection response')
try:
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))


def getPublicKey():
    message = 'GETPUBKEY#'+str(ClientMultiSocket.getsockname()[1])
    ClientMultiSocket.send(str.encode(message))


def register():
    if clientPublicKey == '':
        print('First you have to get your public key')
        getPublicKey()
    else:
        message = 'REGISTER#' + \
            str(ClientMultiSocket.getsockname()[1])+"#"+clientPublicKey
        ClientMultiSocket.send(str.encode(message))


def processResponse(res):
    if res.find("POSTPUBKEY") != -1:
        method, data = res.split("#")
        if method == "POSTPUBKEY":
            global clientPublicKey
            clientPublicKey = data
            print("Recived public key="+data)
        else:
            clientPublicKey = data
            print("Succesfully registered, new public key="+data)
    else:
        print('Server response:'+res)


def communicate():
    partnerid = input("Type the ID of your chat partner")

    message = 'COMMUNICATE#' + \
        str(ClientMultiSocket.getsockname()[1])+"#"+partnerid
    ClientMultiSocket.send(str.encode(message))


res = ClientMultiSocket.recv(1024)
while True:
    task = input(
        'Type the task G (get public key) or R (register) or C (Communicate)')
    if task == "G":
        getPublicKey()
    elif task == "R":
        register()
    else:
        start_new_thread(communicate)

    res = ClientMultiSocket.recv(1024)
    recievedMsg = res.decode('utf-8')
    processResponse(recievedMsg)
ClientMultiSocket.close()

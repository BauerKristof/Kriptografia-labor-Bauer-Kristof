import socket
import os
from _thread import *
import traceback
import crypto as Knapsack

ClientMultiSocket = socket.socket()
host = '127.0.0.1'
port = 2004
clientPublicKey = ''
clientPrivateKey = ''
otherClientPubKey = ''


def GenerateKnapsackKeyPair():
    global clientPublicKey
    global clientPrivateKey

    clientPrivateKey = Knapsack.generate_private_key(8)
    clientPublicKey = Knapsack.create_public_key(clientPrivateKey)


def register():
    GenerateKnapsackKeyPair()
    message = 'REGISTER#' + \
        str(ClientMultiSocket.getsockname()[1])+"#"+str(clientPublicKey)
    ClientMultiSocket.send(str.encode(message))


def getpublickey():
    clientid = input('Type the other client port ID: ')
    message = 'GETPUBKEY#'+str(clientid)
    ClientMultiSocket.send(str.encode(message))


def processResponse(res):
    if res.find("POSTPUBKEY") != -1:
        method, data = res.split("#")
        if data != "NOTFOUND":
            global otherClientPubKey
            otherClientPubKey = data
            print("Recived other client public key="+data)
        else:
            print(
                "The client with the specified ID doesn't exists at the KeyServer, try again")
    else:
        print('Keyserver response:'+res)


def main():
    print('Waiting for connection response')
    try:
        ClientMultiSocket.connect((host, port))
    except socket.error as e:
        print(str(e))

    res = ClientMultiSocket.recv(1024)
    while True:
        task = input(
            'Type the task R (register) or G (get public key) or or C (Communicate)')
        if task == "R":
            register()
        elif task == "G":
            getpublickey()
        else:
            # start_new_thread(communicate)
            print("notimplementedyet")

        res = ClientMultiSocket.recv(1024)
        recievedMsg = res.decode('utf-8')
        processResponse(recievedMsg)
    ClientMultiSocket.close()


if __name__ == "__main__":
    main()

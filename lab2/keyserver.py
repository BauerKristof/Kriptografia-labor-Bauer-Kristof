import socket
import os
from _thread import *
import traceback
import crypto as Knapsack


class ConnectedClient:
    def __init__(self, clientSocket, clientIP, clientPort):
        self.clientSocket = clientSocket
        self.clientIP = clientIP
        self.clientPort = clientPort

    def setPrivateKey(self, privateKey):
        self.privateKey = privateKey

    def setPublicKey(self, publicKey):
        self.publicKey = publicKey


connectedClientsList = []
registeredClientsList = []

ServerSideSocket = socket.socket()
host = '127.0.0.1'
port = 2004
ThreadCount = 0
try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Socket is listening..')
ServerSideSocket.listen(5)


def processMessage(client, message):
    if message.find("GETPUBKEY") != -1:
        method, data = str(message).split("#", 2)
        print("[REQUEST]Get public key - from Client with ID=" +
              str(client.clientPort))
        client.setPrivateKey(Knapsack.generate_private_key(8))
        client.setPublicKey(Knapsack.create_public_key(client.privateKey))
        print("Client "+str(client.clientPort) +
              " got public key:"+str(client.publicKey))

        isInList = False
        for i in connectedClientsList:
            if i.clientPort == client.clientPort:
                isInList = True

        if isInList == False:
            connectedClientsList.append(client)

        return "POSTPUBKEY#"+str(client.publicKey)

    elif message.find("REGISTER") != -1:
        method, clientid, clientpubkey = str(message).split("#", 3)
        print("[REQUEST]REGISTER - from Client with ID=" +
              str(client.clientPort))

        isInList = False
        for i in registeredClientsList:
            if i.clientPort == client.clientPort:
                isInList = True
                client.setPrivateKey(Knapsack.generate_private_key(8))
                client.setPublicKey(
                    Knapsack.create_public_key(client.privateKey))
                break

        if isInList == False:
            registeredClientsList.append(client)

        for i in registeredClientsList:
            print(str(i.clientPort) + " " + str(i.publicKey)+"\n")

        return "POSTPUBKEY#"+str(client.publicKey)


def multi_threaded_client(client):
    try:
        connection = client.clientSocket
        connection.send(str.encode('Server is working:'))
        while True:
            data = connection.recv(2048)
            recievedClientMessage = data.decode('utf-8')
            response = processMessage(client, recievedClientMessage)
            if not data:
                break
            connection.sendall(str.encode(response))
        connection.close()
    except Exception:
        print(traceback.format_exc())


while True:
    Client, address = ServerSideSocket.accept()
    joinedClient = ConnectedClient(Client, address[0], address[1])
    print('Connected to: ' + str(joinedClient.clientIP) +
          ':' + str(joinedClient.clientPort))

    start_new_thread(multi_threaded_client, (joinedClient, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSideSocket.close()

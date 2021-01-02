import socket
import os
from _thread import *
import traceback


class ConnectedClient:
    def __init__(self, clientSocket, clientIP, clientPort):
        self.clientSocket = clientSocket
        self.clientIP = clientIP
        self.clientPort = clientPort

    def setPublicKey(self, publicKey):
        self.publicKey = publicKey


registeredClientsList = []


def multi_threaded_client(client):
    try:
        connection = client.clientSocket
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


def processMessage(client, message):
    if message.find("REGISTER") != -1:
        method, clientid, clientpubkey = str(message).split("#", 3)
        print("[REQUEST]REGISTER - from Client with ID=" +
              str(clientid))

        isInList = False
        for i in registeredClientsList:
            if i.clientPort == clientid:
                isInList = True
                client.setPublicKey(clientpubkey)
                break

        if isInList == False:
            client.clientPort = clientid
            client.setPublicKey(clientpubkey)
            registeredClientsList.append(client)

        for i in registeredClientsList:
            print(str(i.clientPort) + " " + str(i.publicKey)+"\n")
        return "Succesfully registered to KeyServer"

    elif message.find("GETPUBKEY") != -1:
        method, clientid = str(message).split("#", 2)
        print("[REQUEST]Get public key - from Client with ID=" +
              str(client.clientPort))

        isInList = False
        for i in registeredClientsList:
            if str(i.clientPort) == clientid:
                isInList = True
                return "POSTPUBKEY#"+str(i.publicKey)+"#"+str(i.clientPort)

        if isInList == False:
            return "POSTPUBKEY#"+"NOTFOUND#"+"NOTEXISTS"


def main():
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

    while True:
        Client, address = ServerSideSocket.accept()
        joinedClient = ConnectedClient(Client, address[0], address[1])
        print('Connected to: ' + str(joinedClient.clientIP) +
              ':' + str(joinedClient.clientPort))
        print('Becsatlakozott', str(Client.getsockname()[
              1]) + " clientport= "+str(joinedClient.clientPort) + " adress= "+str(address))

        start_new_thread(multi_threaded_client, (joinedClient, ))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
    ServerSideSocket.close()


if __name__ == "__main__":
    main()

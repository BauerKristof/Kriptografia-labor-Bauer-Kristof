import socket
import os
import threading
import traceback
import crypto as Knapsack
import solit as Solitaire
from random import randint, choices
import string
import json
import random


class CommonClass:
    def __init__(self, port):
        if int(port) >= 0:
            self.port = int(port)
            self.host = '127.0.0.1'
            self.initCommunication()

    def initCommunication(self):
        self.actsocket = socket.socket()
        self.actsocket.connect((self.host, self.port))

    def closeConnection(self):
        self.actsocket.close()

    def messageSender(self, message):
        self.actsocket.send(str.encode(message))

    def GenerateKnapsackKeyPair(self):
        clientPrivateKey = Knapsack.generate_private_key(8)
        clientPublicKey = Knapsack.create_public_key(clientPrivateKey)
        return clientPrivateKey, clientPublicKey
    # kozos

    def getpublickey(self, clientid):
        message = 'GETPUBKEY#'+str(clientid)
        self.actsocket.send(str.encode(message))
    # kozos

    def processKeyServerResponse(self, res):
        if res.find("POSTPUBKEY") != -1:
            method, data, portcom = res.split("#")
            if data != "NOTFOUND":
                otherClientPubKey = data
                otherClientPort = portcom
                print("Recived other client public key="+data)
                return str(otherClientPubKey)+"#"+str(otherClientPort)
            else:
                return "ERROR:The client with the specified ID doesn't exists at the KeyServer, try again"
        else:
            return '[KEYSERVER]:Keyserver response:'+res

    def generateRandomSecret(self, deck, ileft, iright):
        i = 0
        while i < 27:
            r = random.randint(ileft, iright)
            if r not in deck:
                deck.append(r)
                i = i+1
        return deck

    def generateCommonKey(self, halfkey1, halfkey2):
        return halfkey1+halfkey2


class KeyServerCommunicator:
    def __init__(self, keyServerPort, listeningClientPort):
        self.keyServerPort = keyServerPort
        self.commonClass = CommonClass(self.keyServerPort)
        self.keyserver_socket = self.commonClass.actsocket
        self.listeningClientPort = listeningClientPort
        self.isRegistered = False
        self.clientPublicKey = ''
        self.clientPrivateKey = ''
        self.otherClientPubKey = ''

    def register(self):
        self.clientPrivateKey, self.clientPublicKey = self.commonClass.GenerateKnapsackKeyPair()
        self.isRegistered = True
        message = 'REGISTER#' + \
            str(self.listeningClientPort)+"#"+str(self.clientPublicKey)
        self.commonClass.messageSender(message)
        self.processResp()

    def communicate(self):
        if self.clientPublicKey == '':
            print("First you have to register to KeyServer")
            self.register()
        elif self.otherClientPubKey == '':
            print("First you have to get the partner's public key")
            clientid = input('Type the other client port ID: ')
            self.commonClass.getpublickey(clientid)
            self.processResp()
        else:
            self.clientDMSender = ClientDMSender(
                self.otherClientPort, self.otherClientPubKey, self.listeningClientPort, self.clientPrivateKey)
            communicator = threading.Thread(
                target=self.clientDMSender.communicateWithOtherClient, args=())
            communicator.start()

    def sendMessageToKeyServer(self):
        task = input(
            'Type the task R (register) or G (get public key) or C (Communicate)')
        if task == "R":
            self.register()
        elif task == "G":
            clientid = input('Type the other client port ID: ')
            self.commonClass.getpublickey(clientid)
            self.processResp()
        elif task == "C":
            self.communicate()

    def processResp(self):
        res = self.keyserver_socket.recv(1024).decode()
        message = self.commonClass.processKeyServerResponse(res)

        if message.find("ERROR") == -1 and message.find("[KEYSERVER]") == -1:
            self.otherClientPubKey, self.otherClientPort = message.split("#")
            print("Recieved chat partner datas:" +
                  self.otherClientPubKey+" "+self.otherClientPort)
        elif message.find("[KEYSERVER]") != -1:
            print(message)
        self.sendMessageToKeyServer()

    def quitClass(self):
        self.commonClass.closeConnection()
        exit()


class ClientDMSender:
    def __init__(self, otherClientPort, otherClientPubKey, listeningClientPort, clientPrivateKey):
        self.otherClientPort = int(otherClientPort)
        self.commonClass = CommonClass(otherClientPort)
        self.otherClientPubKey = otherClientPubKey
        self.listeningClientPort = int(listeningClientPort)
        self.clientPrivateKey = clientPrivateKey
        self.otherclient_socket = self.commonClass.actsocket
        self.succesfullHandShake = False

    def encrypthelper(self, messageToEncrpyt):
        res = eval(self.otherClientPubKey)
        message = Knapsack.encrypt_mh(messageToEncrpyt, res)
        return message

    def decrypthelper(self, messageToDecrypt):
        convertToList = json.loads(messageToDecrypt)
        recievedMsg = Knapsack.decrypt_mh(convertToList, self.clientPrivateKey)
        return recievedMsg

    def communicateWithOtherClient(self):
        message = self.encrypthelper("HI#"+str(self.listeningClientPort))
        self.commonClass.messageSender(str(message))

        while self.succesfullHandShake == False:
            recievedMsg = self.otherclient_socket.recv(
                1024).decode()  # receive response
            recievedMsg = self.decrypthelper(recievedMsg)

            if recievedMsg.find("HEY") != -1:
                command, recievedID = recievedMsg.split('#')
                if int(recievedID) == self.otherClientPort:
                    self.succesfullConnection()

    def succesfullConnection(self):
        print("Succesfull handshake")
        self.succesfullHandShake = True
        halfkey1 = []
        halfkey1 = self.commonClass.generateRandomSecret([], 1, 27)

        print("Sent halfkey1="+str(halfkey1))
        message = self.encrypthelper(str(halfkey1))
        self.commonClass.messageSender(str(message))

        while True:
            halfkey2 = self.otherclient_socket.recv(
                4096).decode()
            halfkey2 = json.loads(self.decrypthelper(halfkey2))
            print("Recieved halfkey2="+str(halfkey2))
            self.commonSecret = self.commonClass.generateCommonKey(
                halfkey1, halfkey2)
            print("The common key is="+str(self.commonSecret))
            self.startChat()

    def solitaireEcryptHelper(self, message):
        prepared_message = self.solit.prep_message(message)
        message_numbers = self.solit.text_to_numbers(prepared_message)
        keystream = self.solit.generate_keystream(len(message_numbers))
        encrypted_message = self.solit.encrypt_message(
            message_numbers, keystream)
        return encrypted_message, len(message_numbers)

    def solitaireDecryptHelper(self, message):
        encriptedMsg, offset = message.split('#')

        encriptedMsg = json.loads(encriptedMsg)
        encriptedMsg = list(map(int, encriptedMsg))

        keystream = self.solit.generate_keystream(int(offset))
        decrypted_message = self.solit.decrypt_message(encriptedMsg, keystream)
        decrypted_message_text = self.solit.numbers_to_text(decrypted_message)
        return decrypted_message_text

    def startChat(self):
        self.solit = Solitaire.SolitaireClass(self.commonSecret)
        isTalking = True

        while isTalking:
            message = input("Please enter a message to encrypt: ")
            encrypted_message, offset = self.solitaireEcryptHelper(message)
            self.commonClass.messageSender(
                str(encrypted_message)+"#"+str(offset))
            msg = self.otherclient_socket.recv(4096).decode()
            decrypted_message_text = self.solitaireDecryptHelper(msg)
            print("Decrypted message:\n", decrypted_message_text)

            if(decrypted_message_text == "BYE"):
                isTalking = False


class ClientDMReciever:
    def __init__(self):
        self.port = randint(1000, 5000)
        self.commonClass = CommonClass(-1)
        self.keyServerCommunicator = KeyServerCommunicator(2004, self.port)
        self.keyserverThread = threading.Thread(
            target=self.keyServerCommunicator.sendMessageToKeyServer, args=())
        self.keyserverThread.start()

        print("Current recieving port="+str(self.port))

    def listen(self):
        self.server_socket = socket.socket()
        self.server_socket.bind(('127.0.0.1', self.port))

        self.server_socket.listen(2)

        self.conn, address = self.server_socket.accept()
        print("Connection from: " + str(address))
        while True:
            data = self.conn.recv(1024).decode()
            if not data:
                break

            if self.keyServerCommunicator.isRegistered == True:
                self.clientPublicKey = self.keyServerCommunicator.clientPublicKey
                self.clientPrivateKey = self.keyServerCommunicator.clientPrivateKey

                recievedMsg = self.decrypthelper(data)
                print("Decrypted message from connected user: " + str(recievedMsg))

                if recievedMsg.find("HI") != -1:
                    command, self.recievedID = recievedMsg.split('#')
                    self.succesfullConnection()
                self.conn.send(data.encode())
        self.conn.close()

    def succesfullConnection(self):
        self.keyServerCommunicator.commonClass.getpublickey(self.recievedID)
        while True:
            res = self.keyServerCommunicator.keyserver_socket.recv(
                1024).decode()
            message = self.keyServerCommunicator.commonClass.processKeyServerResponse(
                res)

            if message.find("ERROR") == -1:
                self.otherClientPubKey, self.otherClientPort = message.split(
                    "#")
                print("Recieved the chatpartner key:" +
                      self.otherClientPubKey+" and id:"+self.otherClientPort)
                message = str(self.encrypthelper("HEY#"+str(self.port)))
                self.conn.send(message.encode())
                self.setCommonKey()

            else:
                print(message)

    def encrypthelper(self, messageToEncrpyt):
        res = eval(self.otherClientPubKey)
        message = Knapsack.encrypt_mh(messageToEncrpyt, res)
        return message

    def decrypthelper(self, messageToDecrypt):
        print("Encrypted message= "+messageToDecrypt)
        convertToList = json.loads(messageToDecrypt)
        recievedMsg = Knapsack.decrypt_mh(convertToList, self.clientPrivateKey)
        return recievedMsg

    def setCommonKey(self):
        while True:
            data = self.conn.recv(4096).decode()

            if not data:
                break

            key1 = json.loads(self.decrypthelper(data))
            print("Decrypted key1 from partner: " + str(key1))
            self.key2 = self.commonClass.generateRandomSecret([], 28, 54)
            print("My key is="+str(self.key2))
            self.commonKey = self.commonClass.generateCommonKey(
                key1, self.key2)
            print("The common key is="+str(self.commonKey))
            message = str(self.encrypthelper(str(self.key2)))
            self.conn.send(message.encode())
            self.startChat()

    def startChat(self):

        self.solit = Solitaire.SolitaireClass(self.commonKey)
        isTalking = True

        while isTalking:
            recievedMsgFromTheClient = self.conn.recv(4096).decode()
            decrypted_message_text = self.solitaireDecryptHelper(
                recievedMsgFromTheClient)
            print("Decrypted message:", decrypted_message_text)

            if(decrypted_message_text == "BYE"):
                isTalking = False

            ownResponse = input("Please enter a message to encrypt: ")
            encrypted_message, offset = self.solitaireEcryptHelper(ownResponse)
            print("Encrypted message="+str(encrypted_message))
            self.conn.send((str(encrypted_message)+"#"+str(offset)).encode())

    def solitaireEcryptHelper(self, message):
        prepared_message = self.solit.prep_message(message)
        message_numbers = self.solit.text_to_numbers(prepared_message)
        keystream = self.solit.generate_keystream(len(message_numbers))
        encrypted_message = self.solit.encrypt_message(
            message_numbers, keystream)
        return encrypted_message, len(message_numbers)

    def solitaireDecryptHelper(self, message):
        encriptedMsg, offset = message.split('#')

        encriptedMsg = json.loads(encriptedMsg)
        encriptedMsg = list(map(int, encriptedMsg))

        keystream = self.solit.generate_keystream(int(offset))
        decrypted_message = self.solit.decrypt_message(encriptedMsg, keystream)
        decrypted_message_text = self.solit.numbers_to_text(decrypted_message)
        return decrypted_message_text


def main():
    clientDMReciever = ClientDMReciever()
    clientDMReciever.listen()


if __name__ == "__main__":
    main()

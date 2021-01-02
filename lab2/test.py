import crypto as Knapsack
import solit as Solitaire
import keyserver as KeyServer
import socket
import threading



def testKnapsackDeck():
    print("2---KNAPSACK TEST FOR DECK ENCRYPTION---")
    pk1=Knapsack.generate_private_key()
    pubkey1=Knapsack.create_public_key(pk1)

    pk2=Knapsack.generate_private_key()
    pubkey2=Knapsack.create_public_key(pk2)


    str1 = ' '.join(str(e) for e in [4, 19, 24, 18, 21, 25, 26, 5, 6, 20, 2, 23, 12, 17, 13, 27, 16, 8, 10, 14, 1, 22, 7, 11, 9, 15, 3])

    print("Message that will be encrypted="+str([4, 19, 24, 18, 21, 25, 26, 5, 6, 20, 2, 23, 12, 17, 13, 27, 16, 8, 10, 14, 1, 22, 7, 11, 9, 15, 3]))
    encripteduzenet=Knapsack.encrypt_mh(str1,pubkey2)
    print("Encrypted message="+str(encripteduzenet))
    decriptaltuzenet=Knapsack.decrypt_mh(encripteduzenet,pk2)
    print("Decrypted message= "+str(decriptaltuzenet))
    print("-----------------------------------------------\n")

def testKnapsackMessage():
    print("1---KNAPSACK TEST FOR MESSAGE ENCRYPTION---")
    pk1=Knapsack.generate_private_key()
    pubkey1=Knapsack.create_public_key(pk1)

    pk2=Knapsack.generate_private_key()
    pubkey2=Knapsack.create_public_key(pk2)

    str1 = "Volt egyszer egy Elek ugy hivtak hogy Teszt Elek aki szerette a teszt eseteket"
    print("Message that will be encrypted="+str1)
    
    encripteduzenet=Knapsack.encrypt_mh(str1,pubkey2)
    print("Encrypted message="+str(encripteduzenet))
    decriptaltuzenet=Knapsack.decrypt_mh(encripteduzenet,pk2)
    print("Decrypted message= "+str(decriptaltuzenet))
    print("-----------------------------------------------\n")

def testSolitaire():
    print("---Solitaire TEST FOR MESSAGE ENCRYPTION---")
    message = "Volt egyszer egy Elek ugy hivtak hogy Teszt Elek aki szerette a teszt eseteket"
    print("Message that will be encrypted="+message)

    deck = [1, 27, 24, 26, 19, 4, 22, 9, 21, 16, 25, 3, 23, 5, 17, 2, 8, 14, 13, 18, 12, 6, 7, 20, 11, 15, 10, 39, 40, 43, 31, 46, 33, 32, 30, 29, 34, 44, 38, 49, 28, 42, 48, 37, 53, 36, 52, 35, 54,51, 47, 45, 41, 50]
    print("Deck:\n", deck)
    
    solit = Solitaire.SolitaireClass(deck)

    prepared_message = solit.prep_message(message)
    print("Message to encrypt:\n", prepared_message)

    message_numbers = solit.text_to_numbers(prepared_message)
    print("Message converted to numbers:\n", message_numbers)
    
    keystream = solit.generate_keystream(len(message_numbers))
    print("Keystream:\n", keystream)
    encrypted_message = solit.encrypt_message(message_numbers, keystream)
    print("Encrypted message:\n", encrypted_message)

    decrypted_message = solit.decrypt_message(encrypted_message, keystream)
    print("Decrypted message, in numbers:\n", decrypted_message)
    decrypted_message_text = solit.numbers_to_text(decrypted_message)
    print("Decrypted message:\n", decrypted_message_text)

def testKeyserver():

    print("Running keyserver")
    keyServer=KeyServer
    
    keyserverThread=threading.Thread(target=keyServer.main, args=())
    keyserverThread.start()

    print("---KEYSERVER REGISTER TEST---")

    print("[TEST]Initializing a client1")
    host='127.0.0.1'
    clientsocket_1 = socket.socket() 
    clientsocket_1.connect((host, 2004))
    
    client1PrivateKey = Knapsack.generate_private_key(8)
    client1PublicKey = Knapsack.create_public_key(client1PrivateKey)
    print("[TEST]Generated Client1 Public and Private Key:",client1PublicKey,client1PrivateKey)
    print("[TEST]Sendig keys to keyserver..")
    message = 'REGISTER#' + str(1)+"#"+str(client1PublicKey)
    clientsocket_1.send(str.encode(message))
    
    keyServerResponseProcesser(clientsocket_1)

    print("[TEST]Initializing a client2")
    clientsocket_2 = socket.socket() 
    clientsocket_2.connect((host, 2004))

    client2PrivateKey = Knapsack.generate_private_key(8)
    client2PublicKey = Knapsack.create_public_key(client2PrivateKey)
    print("[TEST]Generated Client2 Public and Private Key:",client2PublicKey,client2PrivateKey)
    print("[TEST]Sendig keys to keyserver..")
    message = 'REGISTER#' + str(2)+"#"+str(client1PublicKey)
    clientsocket_2.send(str.encode(message))
    keyServerResponseProcesser(clientsocket_2)
    

    print("------------GETTING OTHER CLIENT PUBLIC KEY---------------")
    print("Scenario:Client1 tries to get Client2 public key and port in order to communicate\n")
    message = 'GETPUBKEY#'+str(2)
    clientsocket_1.send(str.encode(message))
    keyServerResponseProcesser(clientsocket_1)

    print("------------GETTING NOT REGISTERED CLIENT PUBLIC KEY---------------")
    print("Scenario:Client1 tries to get a key which not exists\n")
    message = 'GETPUBKEY#'+str(555)
    clientsocket_1.send(str.encode(message))
    keyServerResponseProcesser(clientsocket_1)

    clientsocket_1.close()
    clientsocket_2.close()





def keyServerResponseProcesser(listeningsocket):
    res = listeningsocket.recv(1024).decode()
    if res.find("POSTPUBKEY") != -1:
            method, data, portcom = res.split("#")
            if data != "NOTFOUND":
                otherClientPubKey = data
                otherClientPort=portcom
                print("[TEST]Recived other client public key="+data)
                print(str(otherClientPubKey)+"#"+str(otherClientPort))
            else:
                print( "[TEST]ERROR:The client with the specified ID doesn't exists at the KeyServer, try again")
    else:
        print( '[TEST][KEYSERVER]:Keyserver response:'+res)


def main():
    print("~~~~KNAPSACK TESTS~~~~\n")
    testKnapsackMessage()
    testKnapsackDeck()
    print("~~~~~~~~~~~~~~~~~~~~~~\n")

    print("~~~~SOLITAIRE TESTS~~~~\n")
    testSolitaire()
    print("~~~~~~~~~~~~~~~~~~~~~~\n")

    print("~~~~KEYSERVER TEST~~~~\n")
    testKeyserver()
    print("~~~~~~~~~~~~~~~~~~~~~~\n")

if __name__ == "__main__":
    main()
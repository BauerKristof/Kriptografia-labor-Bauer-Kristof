"""Assignment 1: Cryptography for CS41 Winter 2020.

Name: Bauer Kristof
SUNet: bkim1790

Lab1 Implementation
"""
import string

#################
# CAESAR CIPHER #
#################


def encrypt_caesar(plaintext):
    """Encrypt a plaintext using a Caesar cipher.

    Add more implementation details here.

    :param plaintext: The message to encrypt.
    :type plaintext: str

    :returns: The encrypted ciphertext.
    """

    # Your implementation here.
    charList = []
    charList[:] = plaintext
    ASCII_UPPERS = string.ascii_uppercase
    encryptedText = ""

    for i in charList:
        if not i.isspace():
            if i in string.ascii_uppercase:
                encryptedText += ASCII_UPPERS[(ASCII_UPPERS.index(i)+3) % 26]
            else:
                encryptedText += i
        else:
            encryptedText += i
    return encryptedText


def decrypt_caesar(ciphertext):
    """Decrypt a ciphertext using a Caesar cipher.

    Add more implementation details here.

    :param ciphertext: The message to decrypt.
    :type ciphertext: str

    :returns: The decrypted plaintext.
    """
    # Your implementation here.
    charList = []
    charList[:] = ciphertext
    ASCII_UPPERS = string.ascii_uppercase
    decryptedText = ""

    for i in charList:
        if not i.isspace():
            if i in string.ascii_uppercase:
                decryptedText += ASCII_UPPERS[(ASCII_UPPERS.index(i)-3) % 26]
            else:
                decryptedText += i
        else:
            decryptedText += i
    return decryptedText


def testCaesar():
    print("Encrypt-Caesar\n")
    print(encrypt_caesar("A"))
    print(encrypt_caesar("B"))
    print(encrypt_caesar("I"))
    print(encrypt_caesar("X"))
    print(encrypt_caesar("Z"))
    print(encrypt_caesar("AA"))
    print(encrypt_caesar("TH"))
    print(encrypt_caesar("CAT"))
    print(encrypt_caesar("DOG"))
    print(encrypt_caesar("TOO"))
    print(encrypt_caesar("DAMN"))
    print(encrypt_caesar("DANIEL"))
    print(encrypt_caesar("WHEEEEEE"))
    print(encrypt_caesar("WITH SPACE"))
    print(encrypt_caesar("WITH TWO SPACES"))
    print(encrypt_caesar("NUM83R5"))
    print(encrypt_caesar("0DD !T$"))

    print("\nDecrpyt Caesar\n")
    print(decrypt_caesar("0GG !W$"))
    print(decrypt_caesar("QXP83U5"))
    print(decrypt_caesar("ZLWK WZR VSDFHV"))
    print(decrypt_caesar("ZLWK VSDFH"))


# testCaesar()


###################
# VIGENERE CIPHER #
###################

def encrypt_vigenere(plaintext, keyword):
    """Encrypt plaintext using a Vigenere cipher with a keyword.

    Add more implementation details here.

    :param plaintext: The message to encrypt.
    :type plaintext: str
    :param keyword: The key of the Vigenere cipher.
    :type keyword: str

    :returns: The encrypted ciphertext.
    """
    # Your implementation here.
    textList = []
    codeList = []
    textList[:] = plaintext
    codeList[:] = keyword
    orderOfText = []
    orderOfKeyword = []
    encryptedText = ""

    for i in textList:
        orderOfText.append(ord(i))

    for i in codeList:
        orderOfKeyword.append(ord(i))

    lengthOfKeyword = len(orderOfKeyword)
    print(orderOfText)
    print(orderOfKeyword)

    for i in range(0, len(orderOfText), 1):
        orderOfEncryptedChar = (
            orderOfText[i] + orderOfKeyword[i % lengthOfKeyword])
        abcOrderOfChar = orderOfEncryptedChar % 26
        asciiValueOfEncrpytedChar = chr(abcOrderOfChar+65)
        encryptedText += asciiValueOfEncrpytedChar

    return encryptedText


def decrypt_vigenere(ciphertext, keyword):
    """Decrypt ciphertext using a Vigenere cipher with a keyword.

    Add more implementation details here.

    :param ciphertext: The message to decrypt.
    :type ciphertext: str
    :param keyword: The key of the Vigenere cipher.
    :type keyword: str

    :returns: The decrypted plaintext.
    """
    # Your implementation here.
    textList = []
    codeList = []
    textList[:] = ciphertext
    codeList[:] = keyword
    orderOfText = []
    orderOfKeyword = []
    decryptedText = ""

    for i in textList:
        orderOfText.append(ord(i))

    for i in codeList:
        orderOfKeyword.append(ord(i))

    lengthOfKeyword = len(orderOfKeyword)

    for i in range(0, len(orderOfText), 1):
        orderOfEncryptedChar = (
            orderOfText[i] - orderOfKeyword[i % lengthOfKeyword])
        abcOrderOfChar = orderOfEncryptedChar % 26
        asciiValueOfEncrpytedChar = chr(abcOrderOfChar+65)
        decryptedText += asciiValueOfEncrpytedChar

    return decryptedText


def testVigenere():
    print("Encrypt-Vigenere\n")
    print(encrypt_vigenere("FLEEATONCE", "A"))
    print(encrypt_vigenere("IMHIT", "H"))
    print(encrypt_vigenere("ATTACKATDAWN", "LEMON"))
    print(encrypt_vigenere("WEAREDISCOVERED", "LEMON"))
    print(encrypt_vigenere("SHORTERKEY", "XYZZYZ"))
    print(encrypt_vigenere("A", "ONEINPUT"))
    print("\nDecrypt-Vigenere\n")
    print(decrypt_vigenere("FLEEATONCE", "A"))
    print(decrypt_vigenere("PTOPA", "H"))
    print(decrypt_vigenere("LXFOPVEFRNHR", "LEMON"))
    print(decrypt_vigenere("HIMFROMEQBGIDSQ", "LEMON"))
    print(decrypt_vigenere("PFNQRDOIDX", "XYZZYZ"))
    print(decrypt_vigenere("O", "ONEINPUT"))


# testVigenere()

########################################
# MERKLE-HELLMAN KNAPSACK CRYPTOSYSTEM #
########################################


def generate_private_key(n=8):
    """Generate a private key to use with the Merkle-Hellman Knapsack Cryptosystem.

    Following the instructions in the handout, construct the private key
    components of the MH Cryptosystem. This consists of 3 tasks:

    1. Build a superincreasing sequence `w` of length n
        Note: You can double-check that a sequence is superincreasing by using:
            `utils.is_superincreasing(seq)`
    2. Choose some integer `q` greater than the sum of all elements in `w`
    3. Discover an integer `r` between 2 and q that is coprime to `q`
        Note: You can use `utils.coprime(r, q)` for this.

    You'll also need to use the random module's `randint` function, which you
    will have to import.

    Somehow, you'll have to return all three of these values from this function!
    Can we do that in Python?!

    :param n: Bitsize of message to send (defaults to 8)
    :type n: int

    :returns: 3-tuple private key `(w, q, r)`, with `w` a n-tuple, and q and r ints.
    """
    # Your implementation here.
    raise NotImplementedError('generate_private_key is not yet implemented!')


def create_public_key(private_key):
    """Create a public key corresponding to the given private key.

    To accomplish this, you only need to build and return `beta` as described in
    the handout.

        beta = (b_1, b_2, ..., b_n) where b_i = r × w_i mod q

    Hint: this can be written in one or two lines using list comprehensions.

    :param private_key: The private key created by generate_private_key.
    :type private_key: 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.

    :returns: n-tuple public key
    """
    # Your implementation here.
    raise NotImplementedError('create_public_key is not yet implemented!')


def encrypt_mh(message, public_key):
    """Encrypt an outgoing message using a public key.

    Following the outline of the handout, you will need to:
    1. Separate the message into chunks based on the size of the public key.
        In our case, that's the fixed value n = 8, corresponding to a single
        byte. In principle, we should work for any value of n, but we'll
        assert that it's fine to operate byte-by-byte.
    2. For each byte, determine its 8 bits (the `a_i`s). You can use
        `utils.byte_to_bits(byte)`.
    3. Encrypt the 8 message bits by computing
         c = sum of a_i * b_i for i = 1 to n
    4. Return a list of the encrypted ciphertexts for each chunk of the message.

    Hint: Think about using `zip` and other tools we've discussed in class.

    :param message: The message to be encrypted.
    :type message: bytes
    :param public_key: The public key of the message's recipient.
    :type public_key: n-tuple of ints

    :returns: Encrypted message bytes represented as a list of ints.
    """
    # Your implementation here.
    raise NotImplementedError('encrypt_mh is not yet implemented!')


def decrypt_mh(message, private_key):
    """Decrypt an incoming message using a private key.

    Following the outline of the handout, you will need to:
    1. Extract w, q, and r from the private key.
    2. Compute s, the modular inverse of r mod q, using the Extended Euclidean
        algorithm (implemented for you at `utils.modinv(r, q)`)
    3. For each byte-sized chunk, compute
         c' = cs (mod q)
    4. Solve the superincreasing subset sum problem using c' and w to recover
        the original plaintext byte.
    5. Reconstitute the decrypted bytes to form the original message.

    :param message: Encrypted message chunks.
    :type message: list of ints
    :param private_key: The private key of the recipient (you).
    :type private_key: 3-tuple of w, q, and r

    :returns: bytearray or str of decrypted characters
    """
    # Your implementation here.
    raise NotImplementedError('decrypt_mh is not yet implemented!')

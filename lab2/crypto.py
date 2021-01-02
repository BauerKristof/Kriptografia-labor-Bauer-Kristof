import string
import random
import utils

# Merkle-Hellman Knapsack Cryptosystem


def generate_private_key(n=8):
    """Generate a private key for use in the Merkle-Hellman Knapsack Cryptosystem.
    Following the instructions in the handout, construct the private key components
    of the MH Cryptosystem. This consistutes 3 tasks:
    1. Build a superincreasing sequence `w` of length n
        (Note: you can check if a sequence is superincreasing with `utils.is_superincreasing(seq)`)
    2. Choose some integer `q` greater than the sum of all elements in `w`
    3. Discover an integer `r` between 2 and q that is coprime to `q` (you can use utils.coprime)
    You'll need to use the random module for this function, which has been imported already
    Somehow, you'll have to return all of these values out of this function! Can we do that in Python?!
    @param n bitsize of message to send (default 8)
    @type n int
    @return 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.
    """
    w = tuple(get_super_incr_series(n, 2, 10))
    q = get_next_incr_series(w)
    r = get_coprime(q)
    return w, q, r


def get_super_incr_series(n, i_start, i_end):
    """ Construct a list containing a superincreasing series. List is of length
    n. The first start number is a random number between i_start, and i_end
    inclusive
    """
    start = random.randint(i_start, i_end)
    incr_series = [start]

    while len(incr_series) < n:
        incr_series.append(get_next_incr_series(incr_series))

    return incr_series


def get_next_incr_series(nums):
    """ Takes a super increasing series and returns an integer that is larger
    than the sum of the super increasing series, i.e. a value that could come next
    in the series. The return value is a number between the sum of the series + 1
    and the sum of the series*2
    """
    total = sum(nums)
    return random.randint(total+1, total*2)


def get_coprime(q):
    """ returns a random coprime of q that is less than q.
    """
    r = random.randint(2, q-1)
    while not utils.coprime(q, r):
        r = random.randint(2, q-1)

    return r


def create_public_key(private_key):
    """Create a public key corresponding to the given private key.
    To accomplish this, you only need to build and return `beta` as described in the handout.
        beta = (b_1, b_2, ..., b_n) where b_i = r × w_i mod q
    Hint: this can be written in one line using a list comprehension
    @param private_key The private key
    @type private_key 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.
    @return n-tuple public key
    """
    w, q, r = private_key
    return tuple([(r*w_i) % q for w_i in w])


def encrypt_mh(message, public_key):
    """Encrypt an outgoing message using a public key.
    1. Separate the message into chunks the size of the public key (in our case, fixed at 8)
    2. For each byte, determine the 8 bits (the `a_i`s) using `utils.byte_to_bits`
    3. Encrypt the 8 message bits by computing
         c = sum of a_i * b_i for i = 1 to n
    4. Return a list of the encrypted ciphertexts for each chunk in the message
    Hint: think about using `zip` at some point
    @param message The message to be encrypted
    @type message bytes
    @param public_key The public key of the desired recipient
    @type public_key n-tuple of ints
    @return list of ints representing encrypted bytes
    """

    ciphers = []

    for letter in message:
        bits_arr = utils.byte_to_bits(ord(letter))
        ciphers.append(
            sum([bit*public_key[i] for i, bit in enumerate(bits_arr)])
        )

    return ciphers


def decrypt_mh(message, private_key):
    """Decrypt an incoming message using a private key
    1. Extract w, q, and r from the private key
    2. Compute s, the modular inverse of r mod q, using the
        Extended Euclidean algorithm (implemented at `utils.modinv(r, q)`)
    3. For each byte-sized chunk, compute
         c' = cs (mod q)
    4. Solve the superincreasing subset sum using c' and w to recover the original byte
    5. Reconsitite the encrypted bytes to get the original message back
    @param message Encrypted message chunks
    @type message list of ints
    @param private_key The private key of the recipient
    @type private_key 3-tuple of w, q, and r
    @return bytearray or str of decrypted characters
    """
    w, q, r = private_key

    s = utils.modinv(r, q)

    result = ''

    for chunk in message:
        c_prime = chunk * s % q

        w_rev = w[::-1]
        byte = [0]*len(w)

        for i, w_i in enumerate(w_rev):
            if w_i <= c_prime:
                byte[i] = 1
                c_prime -= w_i

        result += chr(utils.bits_to_byte(byte[::-1]))

    return result

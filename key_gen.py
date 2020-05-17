#key_gen.py

from Crypto.PublicKey import RSA
from Crypto.Util import number
from number_theory import carmichaelFunction, modInv
def generateKeys():                                         # Uses the  RSA library to create private keys.
    key=RSA.generate(2048)                                  # Note public key is included as a subset of this key.
    return key                                              # Recommended key length in bits for RSA is 2048. 

def privateExponent(e, totient):
    d = 1
    for i in range(0, totient):
            d = i
            break
    return bytes(d)

def generateKeys2():                                        # Returns a 2048 bit private key with same prime                                                              
    n_length = 1024                                         # false-positive probability as that of the RSA subroutine.
    e = 65537
    p = number.getStrongPrime(n_length)
    q = number.getStrongPrime(n_length)
    n = p * q
    if (p == q):
        q = number.getStrongPrime(n_length)

    totient = carmichaelFunction(p, q)
    d = modInv(e,totient)
    keys= RSA.construct((n, e, d, p, q))
    return keys
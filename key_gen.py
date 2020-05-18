#key_gen.py
"""
Allows the creation of private keys. The key created by the methods is a private key, 
but as it forms a privatekey object, extraction of a public key is straightforward.

@author: Liam Radley
"""

from Crypto.PublicKey import RSA
from Crypto.Util import number
from number_theory import carmichaelFunction, modInv

def generateKeys(n_length):                                             # Uses the  RSA library to create private keys.
    key=RSA.generate(n_length)                                          # Note public key is included as a subset of this key.
    return key                                                          # Recommended key length in bits for RSA is 2048. 

def generateKeys2(n_length):                                            # Returns a 2048 bit private key with same prime                                                              
    if(n_length < 2048 ):
        print("Key length must be at least 2048 to ensure security.")   
        exit(1)
    e = 65537
    p = number.getStrongPrime(int(n_length / 2))                        # strong prime false-positive probability as that of the RSA subroutine.
    q = number.getStrongPrime(int(n_length / 2))
    if (p == q):
        q = number.getStrongPrime(n_length)
    n = p * q
    totient = carmichaelFunction(p, q)
    d = modInv(e,totient)
    keys= RSA.construct((n, e, d, p, q))
    return keys
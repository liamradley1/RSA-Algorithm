"""
test.py

Contains all tests implemented for ensuring the correctness of subroutines.

@author: Liam Radley
"""
import rsa
import string
import key_gen
from Crypto.Cipher import PKCS1_OAEP
import time

def rsaTest(keys):                                          
    """ Tests the correctness of the implemented RSA algorithm. """
    file = "message.txt"
    plainText = string.ascii_letters + "0123456789"
    rsa.RSAencryptAndSend(plainText, file, keys)
    message = rsa.RSAreadAndDecrypt(file, keys)
    assert(message == plainText)

def paddingTest(paddingCipher):                             
    """ Tests correctness of implemented padding procedures. """
    message = string.ascii_letters+"0123456789"
    file = "message.txt"
    rsa.sendPaddedMessage(message, paddingCipher, file)
    decrypted = rsa.readPaddedMessage(paddingCipher, file)
    message = bytes(message, "utf-8")
    assert (message == decrypted)

def main():
    keys= key_gen.generateKeys(2048)
    cipher=PKCS1_OAEP.new(keys)
    rsaTest(keys)
    paddingTest(cipher)

main()
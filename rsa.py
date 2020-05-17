# -*- coding: utf-8 -*-
"""
Created on Fri May 15 14:05:26 2020

@author: Liam
"""
import string
import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os


def generateKeys():                                         # Uses the RSA library to create private keys.
    key=RSA.generate(1024)                                  # Note public key is included as a subset of this key. 
    return key
                                                        


def getPublicKey(key):
    return key.publickey()

def asciiText(plainText, publicKey):                        # Converts plaintext into ASCII notation, ready for a cipher to be applied. 
    paddedPlainText = [ord(c) for c in plainText]           # Can use any padding cipher.
    return paddedPlainText
    

def characterText(paddedText, publicKey):
    plainText=[chr(c) for c in paddedText]
    return plainText

def rsaEncrypt(keys, padPlain):                             # Encrypts using the RSA algorithm - runs in O(log(n))
    padEncrypt=[pow(m, keys.e, keys.n) for m in padPlain]   # due to built-in modular exponentation function.
    return padEncrypt
    

def rsaDecrypt(keys, padEncrypt):                           
    padDecrypt=[pow(c, keys.d, keys.n) for c in padEncrypt]

    return padDecrypt

def RSAencryptAndSend(plainText, file, key):  
    plainText="b" + plainText                 
    publicKey=getPublicKey(key)                             
    padPlain=asciiText(plainText, publicKey)                   
    padEncrypt=rsaEncrypt(key, padPlain)                    
    padEncrypt=str(padEncrypt)
    f=open(file, "w")
    f.write(padEncrypt)

def RSAreadAndDecrypt(file, key):
    publicKey=getPublicKey(key)
    f=open(file, "r")
    padEncrypt = list(f.read())
    padEncrypt2 = []
    elt2 = ""
    for elt in padEncrypt:
        if(elt.isdigit() == True):
            elt2=elt2 + str(elt)
        else:
            if(elt2 != ""):
                padEncrypt2.append(int(elt2))
                elt2 = ""
    padEncrypt = padEncrypt2
    padDecrypt = rsaDecrypt(key, padEncrypt)
    stringText = characterText(padDecrypt, publicKey)
    plainText = ""
    for i in range(1, len(stringText)):
        plainText = plainText + stringText[i]
    return plainText

def createMessage(plainText, file, keys):
    RSAencryptAndSend(plainText, file, keys)


def rsaTest():
    keys=generateKeys()
    file = "message.txt"
    plainText = string.ascii_letters+"0123456789"
    createMessage(plainText, file, keys)
    message = RSAreadAndDecrypt(file, keys)
    assert(message == plainText)
    
def sendPaddedMessage(message, keys, paddingCipher, file):
    byteMessage=message.encode("utf-8")
    encryptedMessage=paddingCipher.encrypt(byteMessage)
    f=open(file,"wb")
    f.write(encryptedMessage)

def readPaddedMessage(keys, paddingCipher, file):
    f=open(file,"rb")
    paddedMessage = f.read()
    decryptedMessage = paddingCipher.decrypt(paddedMessage)
    return decryptedMessage

def paddingTest(paddingCipher):
    keys = generateKeys()
    message = string.ascii_letters+"0123456789"
    file = "message.txt"
    sendPaddedMessage(message, keys, paddingCipher, file)
    decrypted = readPaddedMessage(keys, paddingCipher, file)
    message = bytes(message, "utf-8")
    assert (message == decrypted)



def main():
    keys = generateKeys()
    padding = PKCS1_OAEP.new(keys)
    rsaTest()
    paddingTest(padding)
    
main()
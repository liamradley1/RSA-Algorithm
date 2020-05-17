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
                                                        

def asciiText(plainText):                                   # Converts plaintext into ASCII representation. 
    paddedPlainText = [ord(c) for c in plainText]           
    return paddedPlainText
    
def characterText(paddedText):                              # Converts ASCII representation back into text.
    plainText=[chr(c) for c in paddedText]
    return plainText

def rsaEncrypt(keys, padPlain):                             # Encrypts directly using the RSA algorithm - runs in O(log(n))
    padEncrypt=[pow(m, keys.e, keys.n) for m in padPlain]   # due to built-in modular exponentation function.
    return padEncrypt                                       # Anyone with public or private key will be able to encrypt data. (keys.n and keys.e are in both)
    

def rsaDecrypt(keys, padEncrypt):                           # Only those with a private key will be able to complete this step.
    padDecrypt=[pow(c, keys.d, keys.n) for c in padEncrypt]

    return padDecrypt

def RSAencryptAndSend(plainText, file, key):                            
    padPlain=asciiText(plainText)                   
    padEncrypt=rsaEncrypt(key, padPlain)                    
    padEncrypt=str(padEncrypt)
    f=open(file, "w")
    f.write(padEncrypt)

def RSAreadAndDecrypt(file, key):
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
    stringText = characterText(padDecrypt)
    plainText = ""
    for i in range(0, len(stringText)):
        plainText = plainText + stringText[i]
    return plainText

def rsaTest():                                              # Tests the correctness of the implemented RSA algorithm.
    keys=generateKeys()
    file = "message.txt"
    plainText = string.ascii_letters+"0123456789"
    RSAencryptAndSend(plainText, file, keys)
    message = RSAreadAndDecrypt(file, keys)
    assert(message == plainText)
    
def sendPaddedMessage(message, keys, paddingCipher, file):
    byteMessage=message.encode("utf-8")                     # Change to byte form to work with padding.
    encryptedMessage=paddingCipher.encrypt(byteMessage)
    f=open(file,"wb")                                       
    f.write(encryptedMessage)

def readPaddedMessage(keys, paddingCipher, file):
    f=open(file,"rb")                                       # Again, our message is in byte form.
    paddedMessage = f.read()
    decryptedMessage = paddingCipher.decrypt(paddedMessage)
    return decryptedMessage

def paddingTest(paddingCipher):                             # Tests to see if the message is actually transmitted and read correctly.
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
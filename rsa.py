# -*- coding: utf-8 -*-
"""
Created on Fri May 15 14:05:26 2020

@author: Liam
"""
import string
import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP as P
import os


def generateKeys():                                         # Uses the RSA library to create private keys.
    key=RSA.generate(1024)                                  # Note public key is included as a subset of this key. 
    return key                                              # Unit test omitted as this only invokes a library subroutine.
                                                            # Any cipher could be used - using PKCS1OAEP here.


def getPublicKey(key):
    return key.publickey()

def padText(plainText, publicKey):                  # Only converts plaintext into ASCII notation. 
    paddedPlainText=[ord(c) for c in plainText]             # Can use any padding cipher.
    return paddedPlainText
    

def unpadText(paddedText, publicKey):                       # Will unit test as a pair in order to ensure correct padding.
    plainText=[chr(c) for c in paddedText]
    return plainText

def rsaEncrypt(keys, padPlain):                             # Encrypts using the RSA algorithm - runs in O(log(n))
    padEncrypt=[pow(m, keys.e, keys.n) for m in padPlain]   # due to built-in modular exponentation function.
    return padEncrypt
    

def rsaDecrypt(keys, padEncrypt):                           
    padDecrypt=[pow(c, keys.d, keys.n) for c in padEncrypt]

    return padDecrypt

def exampleKey():                                           # Provides small test case
    e=5
    p=13
    q=17
    n=13 * 17
    d=77
    components=(n, e, d, p, q)
    key=RSA.construct(components)
    return key

def encryptAndSend(plainText, file, key):                   
    publicKey=getPublicKey(key)                             
    padPlain=padText(plainText, publicKey)                   
    padEncrypt=rsaEncrypt(key, padPlain)                    
    padEncrypt=str(padEncrypt)
    f=open(file, "w")
    f.write(padEncrypt)

def readAndDecrypt(file, key):
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
    stringText = unpadText(padDecrypt, publicKey)
    plainText = ""
    for elt in stringText:
        plainText = plainText + elt
    return plainText

def rsaTest():
    keys=generateKeys()
    file="message.txt"
    plainText=string.ascii_letters+"0123456789"
    createMessage(plainText, keys)
    encryptAndSend(plainText, file, keys)
    message = readAndDecrypt(file, keys)
    assert(message == plainText)


def createMessage(plainText, keys):
    file = "message.txt"
    encryptAndSend(plainText, file, keys)

def main():
    #rsaTest()
    keys=generateKeys()
    message= "Hello, World!"
    file="message.txt"
    createMessage(message, keys)
    print(readAndDecrypt(file, keys))

main()
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 14:05:26 2020

@author: Liam
"""

import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


def generateKeysInHouse(): # Uses the RSA library to create a private key. Note public key is included as a subset of this. 
    key=RSA.generate(1024)
    return key

def generateKeysOSSL():
    os.system('cmd /c "openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:1028 & openssl rsa -pubout -in private_key.pem & openssl rsa -text -in private_key.pem')
    f = open('private_key.pem', 'rb')
    key=RSA.importKey(f.read())
    return key

def padText(plainText):                                     # Only converts plaintext into ASCII notation. 
                                                            # Need to add PKCS1_OAEP padding.
    paddedPlainText=[ord(c) for c in plainText]
    return paddedPlainText

def unpadText(paddedText):
    plainText=[chr(c) for c in paddedText]
    return plainText

def rsaEncrypt(keys,padPlain):                              # Encrypts using the RSA algorithm - runs in O(log(n))
                                                            # due to built-in modular exponentation function.

    padEncrypt=[pow(m,keys.e,keys.n) for m in padPlain]
    return padEncrypt

def rsaDecrypt(keys,padEncrypt):                           
    padDecrypt=[pow(c,keys.d,keys.n) for c in padEncrypt]

    return padDecrypt

def exampleKey():                                           # Provides small test case
    e=5
    p=13
    q=17
    n=13*17
    d=77
    components=(n,e,d,p,q)
    key=RSA.construct(components)
    return key

def main():
    keys=generateKeysInHouse()
    plainText="Hello world!"
    padPlain=padText(plainText)
    print(padPlain)
    padEncrypt=rsaEncrypt(keys,padPlain)  
    padDecrypt=rsaDecrypt(keys,padEncrypt)
    plainText=unpadText(padDecrypt)
    print(plainText)

main()
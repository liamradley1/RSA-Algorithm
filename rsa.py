# -*- coding: utf-8 -*-
"""
Provides the subroutines necessary to encrypt and decrypt using the RSA algorithm,
as well as that of additional PKCS1_OAEP. Note that the two invoke separate methods.

@author: Liam Radley
"""

import string
import time
import key_gen
from Crypto.Cipher import PKCS1_OAEP

def asciiText(plainText):                                   # Converts plaintext into ASCII representation. 
    paddedPlainText = [ord(c) for c in plainText]           
    return paddedPlainText
    
def characterText(paddedText):                              # Converts ASCII representation back into plaintext.
    plainText=[chr(c) for c in paddedText]
    return plainText

def RSAEncrypt(keys, padPlain):                             # Encrypts directly using the RSA algorithm - runs in O(log(n))
    padEncrypt=[pow(m, keys.e, keys.n) for m in padPlain]   # due to built-in modular exponentation function.
    return padEncrypt                                       # Anyone with public or private key will be able to encrypt data. (keys.n and keys.e are in both)
    
def RSADecrypt(keys, padEncrypt):                           # Only those with a private key will be able to complete this step.
    padDecrypt=[pow(c, keys.d, keys.n) for c in padEncrypt]

    return padDecrypt

def RSAencryptAndSend(plainText, file, key):                # Implementation of RSA into 2 key chunks - aids user friendliness.                        
    padPlain=asciiText(plainText)
    padEncrypt=RSAEncrypt(key, padPlain)                    
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
    padDecrypt = RSADecrypt(key, padEncrypt)
    stringText = characterText(padDecrypt)
    plainText = ""
    for i in range(0, len(stringText)):
        plainText = plainText + stringText[i]
    return plainText
    
def sendPaddedMessage(message, keys, paddingCipher, file):  # Separate subroutine for if one aims to work with padding.
    byteMessage=message.encode("utf-8")                     # Change to byte form to work with padding.
    encryptedMessage=paddingCipher.encrypt(byteMessage)
    f=open(file,"wb")                                       
    f.write(encryptedMessage)

def readPaddedMessage(keys, paddingCipher, file):
    f=open(file,"rb")                                       # Again, our message is in byte form.
    paddedMessage = f.read()
    decryptedMessage = paddingCipher.decrypt(paddedMessage)
    return decryptedMessage
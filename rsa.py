# -*- coding: utf-8 -*-
"""
Created on Fri May 15 14:05:26 2020

@author: Liam
"""
import string
import time
import key_gen
import os
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

def rsaTest(keys):                                          # Tests the correctness of the implemented RSA algorithm.
    file = "message.txt"
    plainText = string.ascii_letters + "0123456789"
    RSAencryptAndSend(plainText, file, keys)
    message = RSAreadAndDecrypt(file, keys)
    assert(message == plainText)
    
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

def paddingTest(paddingCipher, keys):                       # Tests to see if the message is actually transmitted and read correctly.
    message = string.ascii_letters+"0123456789"
    file = "message.txt"
    sendPaddedMessage(message, keys, paddingCipher, file)
    decrypted = readPaddedMessage(keys, paddingCipher, file)
    message = bytes(message, "utf-8")
    assert (message == decrypted)

def trackTimes(repetitions):
    startTime=time.time()
    myTimeAvg = 0
    standardTimeAvg = 0
    myTimes = []
    standardTimes = []

    for i in range(0, repetitions):

        time_0 = time.time()                                # Run for the self-implemented subroutine
        keys = key_gen.generateKeys2()
        elapsed = float(time.time() - time_0)
        myTimeAvg += elapsed
        myTimes.append(elapsed)
        padding = PKCS1_OAEP.new(keys)
        paddingTest(padding, keys)                          # Want to ensure that the correct answer is received in each case.

        time_0 = time.time()                                # Run for the standard subroutines.
        keys = key_gen.generateKeys()
        elapsed = float(time.time()-time_0)
        standardTimeAvg += elapsed
        standardTimes.append(elapsed)
        padding = PKCS1_OAEP.new(keys)
        paddingTest(padding, keys)                          # Again, test for correctness.
        
    f=open("times.txt", "w")                                # Write times to file for future reference.
    f.write("My Times, Standard Times \n")                  # Be careful when rerunning experiment - data may be overwritten.
    for i in range(0, repetitions):
        f.write(str(myTimes[i]))
        f.write(",")
        f.write(str(standardTimes[i]))
        f.write("\n")
    f.close()
    myTimeAvg /= repetitions
    standardTimeAvg /= repetitions
    print(f"Average time per iteration on my code: {myTimeAvg} seconds.")
    print(f"Average time per iteration on standard code: {standardTimeAvg} seconds.")
    endTime = time.time() - startTime
    print(f"This experiment took {endTime} seconds.")

def main():
    repetitions = 1000                                      # Choose suitably large iterations to obtain a good running time estimate.
    trackTimes(repetitions)    

main()
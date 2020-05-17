# -*- coding: utf-8 -*-
"""
Created on Fri May 15 14:05:26 2020

@author: Liam
"""
import math
import string
import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os
from Crypto.Util import number


def generateKeys():                                         # Uses the  RSA library to create private keys.
    key=RSA.generate(2048)                                  # Note public key is included as a subset of this key.
    return key                                              # Recommended key length in bits for RSA is 2048. 
                                                  

def gcd(p,q):
    while q != 0:
        t = q
        q = p % q
        p = t
    return int(p)

def lcm(p,q):
    lcm1 =(p*gcd(p,q))*q
    return int(lcm1)

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modInv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def carmichaelFunction(p,q):
    return int(lcm(p-1,q-1))   

def privateExponent(e, totient):
    d=1
    for i in range(0,totient):
            d=i
            break
    return bytes(d)

def generateKeys2():
    """ Gives a 2048 bit private key """                                    
    n_length = 1024
    e = 65537
    primeNum1 = number.getStrongPrime(n_length)
    primeNum2 = number.getStrongPrime(n_length)
    n = primeNum1*primeNum2
    if (primeNum2 == primeNum1):
        primeNum2 = number.getStrongPrime(n_length)

    totient = carmichaelFunction(primeNum1, primeNum2)
    d = modInv(e,totient)
    keys= RSA.construct((n, e, d, primeNum1, primeNum2))
    return keys

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

def rsaTest(keys):                                          # Tests the correctness of the implemented RSA algorithm.
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

def paddingTest(paddingCipher, keys):                       # Tests to see if the message is actually transmitted and read correctly.
    message = string.ascii_letters+"0123456789"
    file = "message.txt"
    sendPaddedMessage(message, keys, paddingCipher, file)
    decrypted = readPaddedMessage(keys, paddingCipher, file)
    message = bytes(message, "utf-8")
    assert (message == decrypted)

def trackTimes(repetitions):
    myTimeAvg=0
    standardTimeAvg=0
    myTimes=[]
    standardTimes=[]
    j=0
    for i in range(0,repetitions):
                                                            # Run for the self-implemented subroutine
        time_0 = time.time()
        keys = generateKeys2()
        elapsed = float(time.time() - time_0)
        myTimeAvg+=elapsed
        myTimes.append(elapsed)
        padding = PKCS1_OAEP.new(keys)
        paddingTest(padding, keys)                          # Want to ensure that the correct answer is received in each case.
        

                                                            # Run for the standard subroutines.
        time_0 = time.time()
        keys = generateKeys()
        elapsed= float(time.time()-time_0)
        standardTimeAvg+=elapsed
        standardTimes.append(elapsed)
        padding = PKCS1_OAEP.new(keys)
        paddingTest(padding, keys)                          # Again, test for correctness.

        
    f=open("times.txt", "w")
    f.write("My Times, Standard Times \n")
    for i in range(0,repetitions):
        f.write(str(myTimes[i]))
        f.write(",")
        f.write(str(standardTimes[i]))
        f.write("\n")
    f.close()
    myTimeAvg/=repetitions
    standardTimeAvg/=repetitions
    print(myTimeAvg)
    print(standardTimeAvg)


def main():
    repetitions = 10
    trackTimes(repetitions)    

main()
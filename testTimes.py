"""
testTimes.py

Creates a file, called "times.txt", filled with information about the length of times taken to run the 
RSA library key generation and self implemented version.

@author: Liam Radley
"""
import time
import key_gen
from Crypto.Cipher import PKCS1_OAEP

def trackTimes(repetitions):
    startTime=time.time()
    myTimeAvg = 0
    standardTimeAvg = 0
    myTimes = []
    standardTimes = []

    for i in range(0, repetitions):

        time_0 = time.time()                                 # Run for the self-implemented subroutine
        keys = key_gen.generateKeys2(2048)
        elapsed = float(time.time() - time_0)
        myTimeAvg += elapsed
        myTimes.append(elapsed)
        padding = PKCS1_OAEP.new(keys)

        time_0 = time.time()                                 # Run for the standard subroutines.
        keys = key_gen.generateKeys(2048)
        elapsed = float(time.time()-time_0)
        standardTimeAvg += elapsed
        standardTimes.append(elapsed)
        padding = PKCS1_OAEP.new(keys)
        
    f=open("times.txt", "w")                                 # Write times to file for future reference.
    f.write("My Times, Standard Times \n")                   # Be careful when rerunning experiment - data may be overwritten.
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
    testing = True
    if(testing == True):
        repetitions = 10
        trackTimes(repetitions)

main()
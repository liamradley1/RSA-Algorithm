"""
number_theoryTest.py

Tests the subroutines implemented in number_theory.py

@author: Liam Radley
"""
import number_theory as nt
import math
import secrets

def gcdTest():
    " A method of checking GCD calculations."
    assert (nt.gcd(0, 0)  == None) # Checks correct definitions for 0,0 case.
    assert (nt.gcd(0, 1)  == 1)    # Checks 0,1 case.
    assert (nt.gcd(1, 3)  == 1)    # Checks 1,(any other number) case.
    assert (nt.gcd(2, 6)  == 2)    # Checks prime, composite case.
    assert (nt.gcd(4, 9)  == 1)    # Checks coprime case.
    assert (nt.gcd(8, 36) == 4)    # Checks 2 composite number case.
    assert (nt.gcd(4, 16) == 4 )   # Check number, square number case.

def eulerTotient(n):    # 
    """ A simple method used for checking the Carmichael Totient, as the Euler Totient is a multiple of the Carmichael Totient.
        Returns the Euler Totient of an integer n. """
    result = 1
    for i in range(2, n): 
        if (nt.gcd(i, n) == 1): 
            result+=1
    return result 

def lcmTest():
    for i in range(0, 5):
        x = secrets.randbelow(2000)
        y = secrets.randbelow(2000)
    
        if x > y:
            greater = x
        else:
            greater = y

        while(True):
            if((greater % x == 0) and (greater % y == 0)):
                lcm = greater
                break
            greater += 1

    assert(lcm == nt.lcm(x,y))

def CarmichaelTest():
    x = secrets.randbelow(2000000)
    y = secrets.randbelow(2000000)
    assert(eulerTotient((x*y)-1) % nt.carmichaelFunction(x,y) == 0)

def modInvTest():
    x = secrets.randbelow(2000000)
    z = secrets.randbelow(4000000)
    y = nt.modInv(x,z)
    assert ((x * y) % z == 1)

def main():
    gcdTest()
    lcmTest()
    CarmichaelTest()
    modInvTest()

    








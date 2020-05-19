"""
key_genTest.py

Tests subroutines implemented in key_gen.py

@author: Liam Radley

"""
import key_gen as kg
import number_theory as nt 
from Crypto.PublicKey import RSA 
import secrets

def attemptSmallKeySize():
    try:
        (kg.generateKeys2(1024) == None)                        # Should throw a ValueError exception
        pass
    except ValueError as identifier:
        return True
        pass

def generateKeys2Test():
    m=secrets.randbelow(256)                                    # ASCII representation will only use up to 255.
    keys = kg.generateKeys2(2048)                               # Will have to take on good faith that subroutine for strong prime does indeed give a strong prime.
    assert (keys.n % keys.p == 0)
    assert (keys.n % keys.q == 0)
    totient = nt.carmichaelFunction(keys.p, keys.q)
    assert ((keys.e * keys.d) % totient == 1 )                  # Check private exponent is calculated correctly
    assert (pow(pow(m, keys.e, keys.n), keys.d, keys.n) == m )  # Assert that modular exponentiation as desired via the method yields correct result.
    assert (attemptSmallKeySize() == True)                      # Assert we actually get the exception for small key sizes.

def main():
    generateKeys2Test()

main()
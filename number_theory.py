#number_theory.py
"""
Provides the necessary numerical machinery to make a private key.

@author: Liam Radley
"""

def gcd(p, q):
    while q != 0:
        t = q
        q = p % q
        p = t
    return int(p)

def lcm(p, q):
    lcm1 =(p * gcd(p, q)) * q
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

def carmichaelFunction(p, q):
    return int(lcm(p-1, q-1))
# RSA Algorithm
- Basic implementation of the RSA Algorithm in Python.

- Also gives a separate implementation using PKCS01_OAEP padding, as basic RSA still allows attributes like the number of a particular character used to be visible.

- Generates keys using subroutine in Python's RSA library, or via a separate method in key_gen.py. 

- Investigation into difference in running times seems to suggest the two are similar in speed, if not that the new method is slightly faster. Both use strongPrime with a tolerance of 1e-6. See supporting "times.txt" for details.
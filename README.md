# RSA Algorithm
- Basic implementation of the RSA Algorithm in Python.

- Also gives a separate implementation using PKCS01_OAEP padding, as basic RSA still allows attributes like the number of occurrences of a   particular character used to be visible.

- Generates keys using subroutine in Python's RSA library, or via a separate method in key_gen.py. 

- Investigation into difference in running times seems to suggest the two subroutines for key generation are similar in speed. Both         generate strong primes with a false positive tolerance of 1e-6. Use testTimes.py to experiment further.

- Unit tests are now implemented. 


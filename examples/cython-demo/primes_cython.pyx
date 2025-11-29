# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
"""Cython implementation of prime number sieve with type declarations."""

import cython
from libc.stdlib cimport malloc, free


def find_primes(int limit):
    """Find all prime numbers up to limit using Sieve of Eratosthenes.

    Uses C-level types and memory for maximum performance.
    """
    cdef int i, j
    cdef int* is_prime
    cdef list primes = []

    if limit < 2:
        return []

    # Allocate C array (much faster than Python list)
    is_prime = <int*>malloc((limit + 1) * sizeof(int))
    if not is_prime:
        raise MemoryError("Failed to allocate memory")

    try:
        # Initialize sieve
        for i in range(limit + 1):
            is_prime[i] = 1
        is_prime[0] = 0
        is_prime[1] = 0

        # Sieve algorithm with typed loop variables
        for i in range(2, <int>(limit ** 0.5) + 1):
            if is_prime[i]:
                for j in range(i * i, limit + 1, i):
                    is_prime[j] = 0

        # Collect primes
        for i in range(2, limit + 1):
            if is_prime[i]:
                primes.append(i)

        return primes
    finally:
        free(is_prime)


def sum_of_primes(int limit):
    """Calculate sum of all primes up to limit."""
    cdef long long total = 0
    cdef int p
    cdef list primes = find_primes(limit)

    for p in primes:
        total += p
    return total

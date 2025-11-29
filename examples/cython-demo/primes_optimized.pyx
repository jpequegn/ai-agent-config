# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
"""Highly optimized Cython implementation using typed memoryviews."""

import numpy as np
cimport numpy as np
from libc.math cimport sqrt

# Compile-time type for numpy arrays
ctypedef np.uint8_t BOOL_t
ctypedef np.int64_t INT64_t


def find_primes_fast(int limit):
    """Optimized sieve using numpy arrays and typed memoryviews."""
    cdef:
        int i, j, sqrt_limit
        np.ndarray[BOOL_t, ndim=1] is_prime
        np.ndarray[INT64_t, ndim=1] primes
        int count = 0

    if limit < 2:
        return np.array([], dtype=np.int64)

    # Use numpy array with memoryview for fast access
    is_prime = np.ones(limit + 1, dtype=np.uint8)
    is_prime[0] = 0
    is_prime[1] = 0

    sqrt_limit = <int>sqrt(<double>limit) + 1

    # Sieve with optimized loop
    for i in range(2, sqrt_limit):
        if is_prime[i]:
            # Start from i*i and mark multiples
            for j in range(i * i, limit + 1, i):
                is_prime[j] = 0

    # Count primes first
    for i in range(2, limit + 1):
        if is_prime[i]:
            count += 1

    # Allocate exact size array
    primes = np.empty(count, dtype=np.int64)
    count = 0
    for i in range(2, limit + 1):
        if is_prime[i]:
            primes[count] = i
            count += 1

    return primes


def sum_of_primes_fast(int limit):
    """Optimized sum calculation."""
    cdef:
        long long total = 0
        np.ndarray[INT64_t, ndim=1] primes
        int i, n

    primes = find_primes_fast(limit)
    n = len(primes)

    for i in range(n):
        total += primes[i]

    return total

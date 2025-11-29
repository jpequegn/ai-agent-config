"""Pure Python implementation of prime number sieve."""


def find_primes(limit: int) -> list[int]:
    """Find all prime numbers up to limit using Sieve of Eratosthenes."""
    if limit < 2:
        return []

    # Initialize sieve
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False

    # Sieve algorithm
    for i in range(2, int(limit ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False

    # Collect primes
    primes = []
    for i in range(2, limit + 1):
        if is_prime[i]:
            primes.append(i)

    return primes


def sum_of_primes(limit: int) -> int:
    """Calculate sum of all primes up to limit."""
    total = 0
    primes = find_primes(limit)
    for p in primes:
        total += p
    return total


if __name__ == "__main__":
    result = find_primes(100)
    print(f"Primes up to 100: {result}")
    print(f"Sum of primes up to 1000: {sum_of_primes(1000)}")

#!/usr/bin/env python3
"""Benchmark comparing Python vs Cython prime number implementations."""

import time
import sys

# Import Python version
from primes_python import find_primes as py_find_primes
from primes_python import sum_of_primes as py_sum_of_primes

# Try to import Cython versions
try:
    from primes_cython import find_primes as cy_find_primes
    from primes_cython import sum_of_primes as cy_sum_of_primes
    CYTHON_AVAILABLE = True
except ImportError:
    print("Cython module not built. Run: python setup.py build_ext --inplace")
    CYTHON_AVAILABLE = False

# Try to import optimized Cython version (uses numpy)
try:
    from primes_optimized import find_primes_fast as opt_find_primes
    from primes_optimized import sum_of_primes_fast as opt_sum_of_primes
    OPTIMIZED_AVAILABLE = True
except ImportError:
    OPTIMIZED_AVAILABLE = False


def benchmark(func, *args, runs: int = 5):
    """Run function multiple times and return average time."""
    times = []
    for _ in range(runs):
        start = time.perf_counter()
        result = func(*args)
        end = time.perf_counter()
        times.append(end - start)
    return sum(times) / len(times), result


def format_time(seconds: float) -> str:
    """Format time in appropriate units."""
    if seconds < 0.001:
        return f"{seconds * 1_000_000:.2f} µs"
    elif seconds < 1:
        return f"{seconds * 1000:.2f} ms"
    else:
        return f"{seconds:.3f} s"


def main():
    limits = [10_000, 100_000, 1_000_000, 10_000_000]
    runs = 3

    print("=" * 70)
    print("Python vs Cython Performance Benchmark: Prime Number Sieve")
    print("=" * 70)
    print()

    for limit in limits:
        print(f"Finding primes up to {limit:,}")
        print("-" * 50)

        # Python benchmark
        py_time, py_result = benchmark(py_find_primes, limit, runs=runs)
        print(f"  Python:  {format_time(py_time):>12}  ({len(py_result):,} primes)")

        if CYTHON_AVAILABLE:
            # Cython benchmark
            cy_time, cy_result = benchmark(cy_find_primes, limit, runs=runs)
            print(f"  Cython:  {format_time(cy_time):>12}  ({len(cy_result):,} primes)")

            # Speedup
            speedup = py_time / cy_time
            print(f"  Speedup: {speedup:.1f}x faster")

            # Verify results match
            if py_result != cy_result:
                print("  WARNING: Results don't match!")

        if OPTIMIZED_AVAILABLE:
            # Optimized Cython benchmark (numpy-based)
            opt_time, opt_result = benchmark(opt_find_primes, limit, runs=runs)
            print(f"  Optimized: {format_time(opt_time):>10}  ({len(opt_result):,} primes)")
            speedup = py_time / opt_time
            print(f"  Speedup: {speedup:.1f}x faster")

        print()

    # Sum of primes benchmark
    print("=" * 70)
    print("Sum of Primes Benchmark")
    print("=" * 70)
    print()

    limit = 1_000_000
    print(f"Sum of primes up to {limit:,}")
    print("-" * 50)

    py_time, py_result = benchmark(py_sum_of_primes, limit, runs=runs)
    print(f"  Python:  {format_time(py_time):>12}  (sum = {py_result:,})")

    if CYTHON_AVAILABLE:
        cy_time, cy_result = benchmark(cy_sum_of_primes, limit, runs=runs)
        print(f"  Cython:  {format_time(cy_time):>12}  (sum = {cy_result:,})")
        speedup = py_time / cy_time
        print(f"  Speedup: {speedup:.1f}x faster")

    if OPTIMIZED_AVAILABLE:
        opt_time, opt_result = benchmark(opt_sum_of_primes, limit, runs=runs)
        print(f"  Optimized: {format_time(opt_time):>10}  (sum = {opt_result:,})")
        speedup = py_time / opt_time
        print(f"  Speedup: {speedup:.1f}x faster")


if __name__ == "__main__":
    main()

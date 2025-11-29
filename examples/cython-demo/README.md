# Python to Cython Conversion Example

This example demonstrates converting a Python script to Cython for performance improvement.

## Files

| File | Description |
|------|-------------|
| `primes_python.py` | Pure Python implementation |
| `primes_cython.pyx` | Cython implementation with type declarations |
| `setup.py` | Build configuration for Cython |
| `benchmark.py` | Performance comparison script |

## Quick Start

```bash
# 1. Install Cython
pip install cython

# 2. Build the Cython extension
cd examples/cython-demo
python setup.py build_ext --inplace

# 3. Run benchmark
python benchmark.py
```

## Key Cython Optimizations

### 1. Type Declarations

```python
# Python (dynamic typing)
def find_primes(limit):
    for i in range(2, limit):
        ...

# Cython (static typing)
def find_primes(int limit):
    cdef int i, j  # C-level integers
    for i in range(2, limit):
        ...
```

### 2. Compiler Directives

```python
# cython: boundscheck=False   # Skip array bounds checking
# cython: wraparound=False    # Disable negative indexing
```

### 3. C Memory Allocation

```python
# Python list (slow)
is_prime = [True] * limit

# C array (fast)
cdef int* is_prime = <int*>malloc(limit * sizeof(int))
```

## Expected Results

Typical speedups for this example:

| Input Size | Python | Cython | Speedup |
|------------|--------|--------|---------|
| 10,000 | ~1 ms | ~0.1 ms | ~10x |
| 100,000 | ~10 ms | ~0.5 ms | ~20x |
| 1,000,000 | ~100 ms | ~5 ms | ~20x |
| 10,000,000 | ~1.5 s | ~50 ms | ~30x |

## When to Use Cython

**Good candidates:**
- Numerical computations with loops
- CPU-bound operations
- Functions called many times
- Code with predictable types

**Less benefit:**
- I/O-bound code
- Code using mostly Python objects
- Simple scripts without hot loops

"""Build script for Cython extensions."""

import numpy as np
from setuptools import setup
from Cython.Build import cythonize

compiler_directives = {
    "language_level": "3",
    "boundscheck": False,
    "wraparound": False,
}

setup(
    name="primes_cython",
    ext_modules=cythonize(
        ["primes_cython.pyx", "primes_optimized.pyx"],
        compiler_directives=compiler_directives,
    ),
    include_dirs=[np.get_include()],
)

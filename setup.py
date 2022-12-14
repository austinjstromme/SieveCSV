from distutils.core import setup, Extension
import os
module = Extension("SieveCSV", sources=["c/sievecsvmodule.c"], include_dirs=["simde"], extra_compile_args=["-Wall", "-O3"])

setup(
    name="SieveCSV",
    version="0.0.1",
    description="Faster CSV parsing with Python",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    ext_modules=[module],
)

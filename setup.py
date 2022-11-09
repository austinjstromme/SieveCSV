from distutils.core import setup, Extension

module = Extension("SieveCSV", sources=["sievecsvmodule.c"], extra_compile_args=["-Wall"])

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

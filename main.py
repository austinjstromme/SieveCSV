from distutils.core import setup, Extension
module1 = Extension("sievecsv", sources = ['sievecsvmodule.c'])
setup(name = "SieveCSV", version = "0.1", description = "SieveCSV: Fast CSV parser", ext_modules = [module1])


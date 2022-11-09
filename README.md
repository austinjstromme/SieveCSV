Faster CSV parsing in Python
----
Austin:
- MacOS 12.5.1
- Python 3.9
- Need apple developer tools installed

Simply run:
python3 setup.py build
python3 setup.py install

Then can use
import SieveCSV

as normal (though will need to add methods in sievecsvmodule.c
in the proper way)

----
Arthur:
- Debian GNU/Linux 11
- Python 3.9
- installed packages python3.9-dev and libpython3.9-dev


To convert `sievecsvmodule.c` to `libsievecsv.so`:
- `gcc $(pkg-config --cflags --libs python3) -Wall -shared -o libsievecsv.so -fPIC sievecsvmodule.c`

To test out the contents of `sievecsvmodule.c`:
- Open up Python REPL.
- `from ctypes import *`
- `import os`
- `cdll.LoadLibrary(os.path.abspath("libsievecsv.so"))`
- `spamLib = CDLL(os.path.abspath("libsievecsv.so"))`
- `spamLib.system`
- `spamLib.system("ls -la")`



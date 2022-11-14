Faster CSV parsing in Python
----
Austin:
- MacOS 12.5.1
- Python 3.9
- Need apple developer tools installed

Simply run:

`python3 setup.py build`

`python3 setup.py install`

Then can use

`import SieveCSV`

as normal (though will need to add methods in sievecsvmodule.c
in the proper way)

---- 
Some design decisions we'll need to make:
- Do we want to make SieveCSV support line-by-line parsing?
- Do we want to do substring filtering or exact filtering or both?


----

Current bugs:

- when the filename passed into parse doesn't refer to an existing file
the module hangs



----
Design, tasks before midterm report:

- Figure out argument parsing (Alan, ideally Wednesday night)
- Source csvs, set up test cases, timing, and demo (Austin, )
	-- matplotlib
- Filter and parse CSV (Alan, Arthur)
	-- Define contract (Thursday)
- Get CSV back out of C into python (Austin, Noah, by weekend)

Tasks for midterm report:
- Write it (Sunday, Monday)

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



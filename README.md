# SieveCSV: 
## Efficient Read-Time CSV Parsing for Database Systems

An implementation of a CSV parser that supports filtering on column equivalence, using ideas from [Sparser](https://www.vldb.org/pvldb/vol11/p1576-palkar.pdf) by Palkar et al. 2018. 

### Installation
* Install C++ and Python. (GCC 10.2.1 and Python 3.9.2 have worked together for Linux / x86.)
* Clone this repository with `git clone --recurse-submodules`.
* On Linux, run `python3 setup.py build` followed by `sudo python3 setup.py install`.
* The library should be importable as `SieveCSV`. 

### Using the library
* The library offers one method currently, which can be used as follows. (The following snippet assumes the existence of a file at path `./data.csv` relative to the current folder.)
```
import SieveCSV
filename = 'data.csv'
rows = SieveCSV.parse_csv(filename, [0, 1], ["6583", "2022"], simd_mode = 3)
```
* `rows` above should then contain a list of lists, where each element of `rows` is a list of the entries of a row of the CSV file at `data.csv`, subject to the condition that the 0th column (0-indexed) is "6583", and the 1st column is "2022".
* `simd_mode` is an optional, keyword-only parameter that represents the time of filtering to use. There are 4 allowed values of `simd_mode`, as follows. (When multiple strings are given to filter on, the first is used for raw filtering.)

| `simd_mode` value | Description |
| ----------------- | ----------- |
| 0 (default)       | Using SIMD to implement a raw filter on the entirety of the string to match on. |
| 1                 | Using SIMD to implement a raw filter on two of the characters of the string to match on. 
| 2                 | Using C's `strstr` to implement a raw filter on the string to match on. |
| 3                 | Using no raw filtering, instead parsing every row and filtering after a row is parsed.|

### Examples
There are a couple places to see how the library works.
* `demo/demo.py` contains an interactive demo of the library in action, as well as to see how timing varies with raw filter use and true positive rate. To run, move to the `demo/` directory and run `python3 demo.py`.
* `tests/` contains some test cases to check library functionality and performance. To run these tests, move to the `tests/` directory.
	- `tests/timing.py` tests the timing of the default parser under different true and false positive rates, for an artificial dataset. It can be run by running `python3 timing.py`, but it may take a long time.
	- `tests/filter.py` tests that the parser is correct with regards to filtering. 
		+ Most of these tests should work out of the box by running `python3 filter.py`. However, one of them, `test_filter_imdb` requires an external dependency too large to host on GitHub. To obtain this dependency, go to [the IMDb Datasets page](https://www.imdb.com/interfaces/), and download `title.basics.tsv.gz` to `csvs/`. Unzip (e.g., using `gzip -d`), and then run `python3 imdb_scripts.py`.
	- `tests/test_imdb.py` tests the timing of the default parser with the IMDb database, using the dependency and data that `tests/filter.py` also uses. See the same bullet to get the dependency for this test.
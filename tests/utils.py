import unittest
import csv
import time

import SieveCSV

"""
Returns true if rowa and rowb
are the same
"""
def same_row(rowa, rowb):
    if len(rowa) != len(rowb):
        return False

    rowzip = zip(rowa, rowb)

    for (a, b) in rowzip:
        if a != b:
            return False

    return True

"""
Filters csv at filename on filters
and cols using python's built-in csv parser
"""
def filter_csv(filename, cols, filters):
    f = open(filename)
    reader = csv.reader(f)

    zipped_filters_cols = list(zip(filters, cols))

    result = []

    for row in reader:
        passes_filters = True

        for (filt, i) in zipped_filters_cols:
            if i >= len(row):
                continue
            if filt not in row[i]:
                passes_filters = False
                break

        if passes_filters:
            result.append(row)

    f.close()

    return result

"""
Compares the output of SieveCSV with the
output of python's csv parser on a csv file

testcase (unittest.TestCase) testcase to throw errows with
filename (string)            csv file to filter and parse
filters (list of strings)    filters to apply
rows (list of integers)      rows to apply filter to

Applies filters[i] at row rows[i]

Uses testcase to assert that SieveCSV and python return the same thing

boolean, list of lists, list of lists
"""
def compare_output(testcase, filename, cols, filters):
    sievecsvfiltered = SieveCSV.parse_csv(filename, cols, filters)

    pyfiltered = filter_csv(filename, cols, filters)

    sieve_len = len(sievecsvfiltered)
    py_len = len(pyfiltered)

    sieve_rows = set()
    py_rows = set()
    MAX_ROWS_CHECKED = 20
    num_rows_to_check = max(sieve_len, py_len)

    diff_col_counts = ""
    for i in range(num_rows_to_check):
        if i < sieve_len:
            sieve_rows.add(tuple(sievecsvfiltered[i]))
        if i < py_len:
            py_rows.add(tuple(pyfiltered[i]))
        if i < py_len and i < sieve_len:
            if len(pyfiltered[i]) != len(sievecsvfiltered[i]):
                diff_col_counts = f"Found that Python returned row with {len(pyfiltered[i])} columns, while SieveCSV returned row with {len(sievecsvfiltered[i])} columns. "

    sieve_not_py = sieve_rows - py_rows
    py_not_sieve = py_rows - sieve_rows

    fail = False
    length_msg = ""
    if sieve_len > py_len:
        length_msg = "SieveCSV returns more rows than Python. "
        fail = True
    elif sieve_len < py_len:
        length_msg = "Python returns more rows than SieveCSV. "
        fail = True
    else:
        length_msg = "SieveCSV and Python return the same number of rows. "

    diff_msg = ""
    if len(sieve_not_py) != 0:
        sieve_bad_row = None
        for row in sieve_not_py:
            sieve_bad_row = row
            break
        diff_msg += f"SieveCSV returns row {sieve_bad_row}, which is not returned by Python. "
        fail = True
    if len(py_not_sieve) != 0:
        py_bad_row = None
        for row in py_not_sieve:
            py_bad_row = row
            break
        diff_msg += f"SieveCSV did not return row {py_bad_row}, which was returned by Python. "
        fail = True

    cols_and_filters = f"Columns requested were {cols}. Filters requested were {filters}. "
    row_nums = f"SieveCSV returned {sieve_len} rows, while Python returned {py_len} rows. "
    testcase.assertTrue(not fail, length_msg + row_nums + diff_msg + cols_and_filters + diff_col_counts)   

"""
Runs compare_output on each argument tuple
in filenames, cols, filters zipped together
"""
def compare_output_multiple(testcase, filenames, cols, filters):
        zippedargs = zip(filenames, cols, filters)

        for fname, collist, filterlist in zippedargs:
            compare_output(testcase, fname, collist, filterlist)

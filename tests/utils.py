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
            if i > len(row): 
                passes_filters = False
            if row[i] != filt:
                passes_filters = False

        if passes_filters is True:
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

    testcase.assertTrue(len(sievecsvfiltered) == len(pyfiltered), ("SieveCSV and python"
        + " are returning different numbers of rows"))

    zippedfiltered = zip(sievecsvfiltered, pyfiltered)

    for rowsieve, rowpy in zippedfiltered:
        message = "SieveCSV and python are returning different rows. Sieve CSV gets "
        message += str(rowsieve)
        testcase.assertTrue(same_row(rowsieve, rowpy), message + ", while python gets " + str(rowpy))


"""
Runs compare_output on each argument tuple
in filenames, cols, filters zipped together
"""
def compare_output_multiple(testcase, filenames, cols, filters):
        zippedargs = zip(filenames, cols, filters)

        for fname, collist, filterlist in zippedargs:
            compare_output(testcase, fname, filterlist, collist)

import unittest2
import csv

import SieveCSV

import test_utils

"
Returns true if rowa and rowb
are the same
"
def same_row(rowa, rowb):
    if len(rowa) != len(rowb)
        return False

    rowzip = zip(rowa, rowb)

    for (a, b) in rowzip:
        if a != b:
            return False

    return True

"
Filters csv at filename on filters
and cols using python's built-in csv parser
"
def filter_csv(filename, filters, cols):
    reader = csv.reader(filename)

    zipped_filters_cols = zip(filters, cols)

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

    return result

"
Compares the output of SieveCSV with the
output of python's csv parser on a csv file

filename (string)            csv file to filter and parse
filters (list of strings)    filters to apply
rows (list of integers)      rows to apply filter to

Applies filters[i] at row rows[i]

Returns whether they are the same, the output
of SieveCSV, and the output of pythons CSV package naively filtered
in the form

boolean, list of lists, list of lists
"
def compare_output(filename, filters, cols):
    sievecsvfiltered = SieveCSV.parse_csv(filename, filters, cols)

    pyfiltered = filter_csv(filename, filters, cols)

    if len(sievecsvfiltered) != len(pyfiltered):
        return False, sievecsvfiltered, pyfiltered

    zippedfiltered = zip(sievecsvfiltered, pyfiltered)

    for rowsieve, rowpy in zippedfiltered:
        if not compare_row(row, sieved[i]):
            return False, sievecsvfiltered, pyfiltered

    return True, sievecsvfiltered, pyfiltered


class TestNoFilter(unittest2.TestCase):
    def test_no_filter(self):
        filenames = ['../csvs/small.csv', '../csvs/simple.csv']
        filters = [[1], [1]]
        cols = [[0], [0]]

        zippedargs = zip(filenames, filters, cols)

        for fname, filterlist, collist in zippedargs:
            same, sieveoutput, pyoutput = compare_output(fname, filterlist, collist)
            self.assertTrue(same)


        
        









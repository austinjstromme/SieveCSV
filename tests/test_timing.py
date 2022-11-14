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
def filter_csv(filename, filters, cols):
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

filename (string)            csv file to filter and parse
filters (list of strings)    filters to apply
rows (list of integers)      rows to apply filter to

Applies filters[i] at row rows[i]

Returns whether they are the same, the output
of SieveCSV, and the output of pythons CSV package naively filtered
in the form

boolean, list of lists, list of lists
"""
def timing_loop(iterations, filename = "../csvs/small.csv", filters = ["1"], cols = [0]):
    s_csv_time = 0
    py_csv_time = 0
    for _ in range(iterations):
        s_csv_start = time.time()
        sievecsvfiltered = SieveCSV.parse_csv(filename, cols, filters)
        s_csv_end = time.time()
        s_csv_time += s_csv_end - s_csv_start

        py_csv_start = time.time()
        pyfiltered = filter_csv(filename, filters, cols)
        py_csv_end = time.time()
        py_csv_time += py_csv_end - py_csv_start

        if len(sievecsvfiltered) != len(pyfiltered):
            print(sievecsvfiltered)
            print(pyfiltered)
            raise Exception("did not match! " + str(_))

        zippedfiltered = zip(sievecsvfiltered, pyfiltered)

        for rowsieve, rowpy in zippedfiltered:
            if not same_row(rowsieve, rowpy):
                raise Exception("did not match!")

    return (s_csv_time, py_csv_time)

if __name__ == "__main__":
    print(timing_loop(32000))
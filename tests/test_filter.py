import unittest
import csv
import time

import utils
import SieveCSV

class TestFilter(unittest.TestCase):
    def test_no_filter_small(self):
        filenames = ['../csvs/small.csv', '../csvs/simple.csv']
        filters = [[], []]
        cols = [[], []]

        zippedargs = zip(filenames, filters, cols)

        for fname, filterlist, collist in zippedargs:
            utils.compare_output(self, fname, filterlist, collist)

    def test_filter_small(self):
        filenames = ['../csvs/small.csv', '../csvs/simple.csv', '../csvs/simple.csv']
        filters = [['1'], ['a'], ['c']]
        cols = [[0], [2], [2]]

        zippedargs = zip(filenames, filters, cols)

        for fname, filterlist, collist in zippedargs:
            utils.compare_output(self, fname, filterlist, collist)


    def test_no_filter_large(self):
        filenames = ['../csvs/randomlarge.csv']
        filters = [[]]
        cols = [[]]

        zippedargs = zip(filenames, filters, cols)

        for fname, filterlist, collist in zippedargs:
            utils.compare_output(self, fname, filterlist, collist)

    def test_filter_large(self):
        filenames = ['../csvs/randomlarge.csv']
        filters = [['1']]
        cols = [[10]]

        zippedargs = zip(filenames, filters, cols)

        for fname, filterlist, collist in zippedargs:
            utils.compare_output(self, fname, filterlist, collist)

if __name__ == '__main__':
    test_loader = unittest.defaultTestLoader

    test_runner = unittest.TextTestRunner()

    test_suite = test_loader.discover('.')

    test_runner.run(test_suite)

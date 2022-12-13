import time

import utils
import csv

DEFAULT_RATES = [0.001, 0.01, 0.1, 0.25, 0.5]

def test_timing(iterations, filename, filters, cols):
    return utils.timing_loop(iterations, filename, filters, cols)

def main():
    res, res_port = utils.timing_loop(2, "../csvs/title.basics.short.csv", ['1895'], [5])

    print("res = " + str(res))
    print("res_port = " + str(res_port))

if __name__ == '__main__':
    main()

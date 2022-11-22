import time

import utils
import SieveCSV

def test_timing(iterations, filename = "../csvs/small.csv", filters = ["1"], cols = [0]):
    s_csv_time, py_csv_time = utils.timing_loop(iterations, filename, filters, cols)
    return f"we took: {s_csv_time}, they took: {py_csv_time}"

if __name__ == "__main__":
    print(test_timing(100, filename="../csvs/randomlarge.csv"))
    print(test_timing(100, filename="../csvs/randomlarge.csv", filters=["Albertan"], cols=[6]))
    print(test_timing(100, filename="../csvs/randomlarge_selective.csv", filters=["Albertan"], cols=[6]))
    print(test_timing(10000, filters = [], cols = []))
    print(test_timing(10000))

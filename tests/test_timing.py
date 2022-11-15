import time

import test_utils as utils
import SieveCSV

def timing_loop(iterations, filename = "../csvs/small.csv", filters = ["1"], cols = [0]):
    s_csv_time = 0
    py_csv_time = 0
    for _ in range(iterations):
        s_csv_start = time.time()
        sievecsvfiltered = SieveCSV.parse_csv(filename, cols, filters)
        s_csv_end = time.time()
        s_csv_time += s_csv_end - s_csv_start

        py_csv_start = time.time()
        pyfiltered = utils.filter_csv(filename, cols, filters)
        py_csv_end = time.time()
        py_csv_time += py_csv_end - py_csv_start

        if len(sievecsvfiltered) != len(pyfiltered):
            print(sievecsvfiltered)
            print(pyfiltered)
            raise Exception("did not match! " + str(_))

        zippedfiltered = zip(sievecsvfiltered, pyfiltered)

        for rowsieve, rowpy in zippedfiltered:
            if not utils.same_row(rowsieve, rowpy):
                raise Exception("did not match!")

    return (s_csv_time, py_csv_time)

if __name__ == "__main__":
    #print(timing_loop(5, filename="../csvs/randomlarge.csv", filters = [], cols = []))
    print(timing_loop(500, filters = [], cols = []))

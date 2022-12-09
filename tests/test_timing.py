import time

import utils
import SieveCSV

def test_timing(iterations, filename = "../csvs/small.csv", filters = ["1"], cols = [0]):
    return utils.timing_loop(iterations, filename, filters, cols)

if __name__ == "__main__":
    # print(test_timing(100, filename="../csvs/randomlarge.csv"))
    print(test_timing(100, filename="../csvs/randomlarge.csv", filters=["6626"], cols=[4]))
        # print(simd_mode, test_timing(100, filename="../csvs/randomlarge.csv", filters=["Albertan"], cols=[6], simd_mode=simd_mode))
        # print(simd_mode, test_timing(1000, filename="../csvs/randomlong-narrow.csv", filters=["Albertan"], cols=[6], simd_mode=simd_mode))
    # print(test_timing(100, filename="../csvs/randomlarge.csv", filters=["Albertan"], cols=[6]))
    # print(test_timing(100, filename="../csvs/randomlarge_selective.csv", filters=["Albertan"], cols=[6]))
    # print(test_timing(10000, filters = [], cols = []))
    # print(test_timing(10000))

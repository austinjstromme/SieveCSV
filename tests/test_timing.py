import time

import utils
import csv

def test_timing(iterations, filename = "../csvs/small.csv", filters = ["1"], cols = [0]):
    return utils.timing_loop(iterations, filename, filters, cols)

if __name__ == "__main__":
    with open("results.csv", "w", newline='') as f:
        writer = csv.writer(f, lineterminator="\n")
        for FPRATE in [0.25, 0.5]:
            for TPRATE in [0.001, 0.01, 0.1, 0.25, 0.5]:
                res = test_timing(100, filename=f"../csvs/testing/randomlarge-fp-{FPRATE}-tp-{TPRATE}.csv", filters=["6626"], cols=[0])
                row = [FPRATE, TPRATE]
                for r in res:
                    row.append(r[0])
                    row.append(r[1])
                    row.append(r[2])
                writer.writerow(row)
                print(FPRATE, TPRATE)
                f.flush()
            

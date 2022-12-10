import csv
import numpy as np

# randomlarge (width 100, length 10000)
# randomlong-narrow (width 10, length 10000)
WIDTH = 100
LENGTH = 10000
RANGE = 10000

np.random.seed(0)
for FPRATE in [0.001, 0.01, 0.1, 0.25, 0.5]:
    for TPRATE in [0.001, 0.01, 0.1, 0.25, 0.5]:
        with open(f"testing/randomlarge-fp-{FPRATE}-tp-{TPRATE}.csv", "w", newline='') as f:
            writer = csv.writer(f, lineterminator="\n")

            for l in range(0, LENGTH):
                row = [np.random.randint(RANGE) for j in range(0, WIDTH)]
                if np.random.random() < FPRATE: 
                    row[50] = 6626
                if np.random.random() < TPRATE:
                    row[0] = 6626
                writer.writerow(row)


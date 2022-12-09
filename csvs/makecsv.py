import csv
import numpy as np

# randomlarge (width 100, length 10000)
# randomlong-narrow (width 10, length 10000)
WIDTH = 10
LENGTH = 10000
RANGE = 10000

np.random.seed(0)

with open("randomlong-narrow.csv", "w", newline='') as f:
    writer = csv.writer(f, lineterminator="\n")

    for l in range(0, LENGTH):
        writer.writerow([np.random.randint(RANGE) for j in range(0, WIDTH)])


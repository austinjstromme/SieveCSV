import csv
import numpy as np

WIDTH = 100
LENGTH = 10000
RANGE = 100

np.random.seed(0)

with open("randomlarge.csv", "w", newline='') as f:
    writer = csv.writer(f, lineterminator="\n")

    for l in range(0, LENGTH):
        writer.writerow([np.random.randint(RANGE) for j in range(0, WIDTH)])


import csv
import numpy as np

WIDTH = 100
LENGTH = 10000
RANGE = 999

np.random.seed(0)

with open("largecsvrandom.csv", "w", newline='') as f:
    writer = csv.writer(f)

    for l in range(0, LENGTH):
        writer.writerow([np.random.randint(100) for j in range(0, WIDTH)])


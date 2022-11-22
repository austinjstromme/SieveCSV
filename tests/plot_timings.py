import time
import numpy as np
import matplotlib.pyplot as plt

import utils
import SieveCSV

ITERATIONS = 20
randomlarge = "../csvs/randomlarge.csv"
randomlarge_selective = "../csvs/randomlarge_selective.csv"

filelist = [randomlarge, randomlarge, randomlarge, randomlarge]
filterlist = [[], ["1"], ["1", "1"], ["1", "1", "1"]]
# each filter should be a constant factor more selective than the last
colslist = [[], [0], [0, 1], [0, 1, 2]]  

zippedargs = zip(filelist, filterlist, colslist)

sieve_times = []
py_times = []
for file, filters, cols in zippedargs:
    sieve_t, py_t = utils.timing_loop(ITERATIONS, filename=randomlarge, filters=filters, cols=cols)
    sieve_times.append(sieve_t)
    py_times.append(py_t)

print("sieve times = " + str(sieve_times))
print("py times = " + str(py_times))

selectivities=[1.*((.7)**i) for i in range(0, 4)]
# this is a rough heuristic for the selectivity of our filters

plt.plot(selectivities, sieve_times, label='SieveCSV')
plt.plot(selectivities, py_times, label='PythonCSV')

plt.xlabel('Selectivity of the filter')
plt.ylabel('Time over ' + str(ITERATIONS) + ' runs')

plt.title('SieveCSV vs PythonCSV on large random CSV file')
plt.legend()

plt.show()




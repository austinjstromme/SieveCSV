import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

vals = []
a = csv.reader(open("results-0.csv", "r"), delimiter="\t")
for line in a:
    vals.append(line)

vals = [[float(val) for val in row] for row in vals]
vals_fp = [row for row in vals if row[1] == 0.01]

fig, ax = plt.subplots()
plt.errorbar([row[0] for row in vals_fp], [row[2] for row in vals_fp], yerr=[1.96*row[3] for row in vals_fp], fmt="-o", label="SIMD strstr pre-filter")
plt.errorbar([row[0] for row in vals_fp], [row[4] for row in vals_fp], yerr=[1.96*row[5] for row in vals_fp], fmt="-o", label="mixed C/SIMD pre-filter")
plt.errorbar([row[0] for row in vals_fp], [row[6] for row in vals_fp], yerr=[1.96*row[7] for row in vals_fp], fmt="-o", label="C strstr pre-filter")
plt.errorbar([row[0] for row in vals_fp], [row[8] for row in vals_fp], yerr=[1.96*row[9] for row in vals_fp], fmt="-o", label = "SieveCSV parser")
plt.errorbar([row[0] for row in vals_fp], [row[10] for row in vals_fp], yerr=[1.96*row[11] for row in vals_fp], fmt="-o", label="Python parser")
plt.xscale('log')
plt.xticks([0.001, 0.01, 0.1, 0.25, 0.5])
ax.xaxis.set_major_formatter(ScalarFormatter())
ax.set_xlabel("False positive rate")
ax.set_ylabel("Time per query (s)")
plt.title("SieveCSV performance at true positive rate = 0.01")
plt.legend()
plt.show()
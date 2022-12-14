#import time
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

import utils
import csv

def test_timing(iterations, filename, filters, cols):
    return utils.timing_loop(iterations, filename, filters, cols)

def gather_selectivities(write=False):
    f = open("../csvs/title.basics.csv")

    total_lines = 0
    year_counts = {}

    reader = csv.reader(f)
    # skip first line describing data
    reader.__next__()

    for row in reader:
        total_lines += 1

        #print("row[5] = " + str(row[5]))
        year = -1

        try:
            year = int(row[5])
        except ValueError:
            year = -1

        if year in year_counts.keys():
            year_counts[year] = year_counts[year] + 1
        else:
            year_counts[year] = 1

    # remove count for any year entries that were not integers
    total_lines -= year_counts[-1]

    if write:
        fout = open("imdb_year_stats.csv", "w", newline='')
        writer = csv.writer(fout, lineterminator="\n")

        for key in year_counts.keys():
            writer.writerow([key, year_counts[key]/total_lines])

        fout.close()

    f.close()

    return year_counts, total_lines

def plot_data():
    year_counts, total_lines = gather_selectivities()
    f = open("imdb_results.csv", "r", newline='')

    vals = []
    a = csv.reader(f, delimiter=",")
    for line in a:
        # only take the rows that had outliers removed
        if int(line[0]) == 1:
            row = [int(line[1]), float(line[2]), float(line[3]),float(line[11]),float(line[12]),float(line[14]), float(line[15])]
            vals.append(row)

    print("vals = " + str(vals))

    for row in vals:
        print("year = " + str(row[0]))
        print("year_counts = " + str(year_counts[row[0]]))
    
    fig, ax = plt.subplots()
    plt.errorbar([float(year_counts[row[0]])/total_lines for row in vals], [row[1] for row in vals], yerr=[1.96*row[2] for row in vals], fmt="-o", label="SIMD strstr pre-filter")
    plt.errorbar([float(year_counts[row[0]])/total_lines for row in vals], [row[3] for row in vals], yerr=[1.96*row[4] for row in vals], fmt="-o", label="SieveCSV parser")
    plt.errorbar([float(year_counts[row[0]])/total_lines for row in vals], [row[5] for row in vals], yerr=[1.96*row[6] for row in vals], fmt="-o", label="Python parser")

    plt.xscale('log')
    #plt.xticks([0.001, 0.01, 0.1, 0.25, 0.5])
    ax.xaxis.set_major_formatter(ScalarFormatter())
    ax.set_xlabel("Selectivity")
    ax.set_ylabel("Time per query (s)")
    plt.title("SieveCSV performance on IMDB title year selection queries")
    plt.legend()
    plt.show()

    f.close()

def gather_data():
    #year_counts = gather_selectivities()
    # years = year_counts.keyset()
    years = [1893,1892,1894,1900,1951,1987,2009,2020]

    fout = open("imdb_results.csv", "w", newline='')
    writer = csv.writer(fout, lineterminator="\n")

    year_timings = {}

    for year in years:
        res, res_post = utils.timing_loop(3, filename=f"../csvs/title.basics.csv", filters=[str(year)], cols=[5], simd_modes=[0, 3])
        year_timings[year] = [res, res_post]

        row = [0, year]
        for r in res:
            row.append(r[0])
            row.append(r[1])
            row.append(r[2])
        writer.writerow(row)

        row = [1, year]
        for r in res_post:
            row.append(r[0])
            row.append(r[1])
            row.append(r[2])
        writer.writerow(row)

    print(year_timings)

    fout.close()

def main():
    # gather_data()
    plot_data()
    #gather_selectivities(write=True)
    # res, res_port = utils.timing_loop(2, "../csvs/title.basics.csv", ['1895'], [5])

    #with open("imdb_results.csv", "w", newline='') as f:
    #    writer = csv.writer(f, lineterminator="\n")
    #    res, res_post = test_timing(5, filename=f"../csvs/title.basics.short.csv",
    #            ['1895'], [5])


if __name__ == '__main__':
    main()

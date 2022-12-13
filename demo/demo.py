import csv
import numpy as np
import random
import time
from os import system, name
import SieveCSV
import sys
def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def prompt():
    _ = input("[press enter to continue]\n")
    sys.stdout.write("\033[2F")
    

def get_input_in_range(low, high):
    val = None
    while True:
        str_val = input(f"Choose a number from {low} to {high}: ")
        maybe_val = None
        try: 
            maybe_val = int(str_val)
        except:
            pass
        if maybe_val is None:
            print(f"Input \"{str_val}\" couldn't be parsed as an integer. Try again.")
            continue
        elif maybe_val < low or maybe_val > high:
            print(f"{maybe_val} isn't in range. Try again.")
            continue
        good_val = input(f"Confirm {maybe_val}? Enter something with a 'Y' to confirm, or anything else to try again: ")
        if "Y" in good_val:
            val = maybe_val
            break
        else:
            continue
    return val

def make_small_demo_csv(num_positive = 1, special_value=7, filename="randomsmall.csv"):
    def some_value(nothing_special):
        while True:
            ans = random.randint(0, 9)
            if nothing_special and ans == special_value:
                continue
            else:
                return ans
    num_cols = 8
    num_rows = 8
    random.seed()
    positive_rows = random.sample(range(0, num_rows), num_positive)
    with open(filename, "w", newline='') as f:
        writer = csv.writer(f, lineterminator="\n")
        row = None
        for i in range(num_rows):
            row = [some_value(i == 0) for i in range(num_cols)]
            if i in positive_rows: # make positive row
                row[0] = special_value 
            writer.writerow(row)

    with open(filename) as f:
        f_data = f.read()
        print(f"The file {filename} has been written to with contents: ")
        print(f_data)

    return filename

def make_large_demo_csv(frac_positive = 0, special_value=4444, filename="randomlarge.csv"):
    def some_value(not_special):
        while True:
            ans = random.randint(1000, 9999)
            if not_special and ans == special_value:
                continue
            else:
                return ans

    num_cols = 8
    num_rows = 10000
    random.seed()
    positive_rows = random.sample(range(0, num_rows), 0 if frac_positive < 0.0001 else int(1.0 * frac_positive * num_rows))
    actual_positive_rows = 0

    sample_rows = []
    with open(filename, "w", newline='') as f:
        writer = csv.writer(f, lineterminator="\n")
        row = None
        for i in range(num_rows):
            row = [some_value(i == 0) for i in range(num_cols)]
            if i in positive_rows: # make positive row
                row[0] = special_value 
            if row[0] == special_value:
                actual_positive_rows += 1
            writer.writerow(row)
            if (len(sample_rows) < 3):
                sample_rows += [row]
    
    print(f"The file {filename} has been written to.")    
    print(f"Some of the rows contained therein are: ")
    for row in sample_rows:
        print(f"\t{row}")

    return (filename, actual_positive_rows)

# copied mostly from the utils library we wrote in the tests/ directory
def filter_csv(filename, cols=[], filters=[]):
    f = open(filename)
    reader = csv.reader(f)

    zipped_filters_cols = list(zip(filters, cols))

    result = []

    for row in reader:
        passes_filters = True

        for (filt, i) in zipped_filters_cols:
            if i >= len(row):
                continue
            if filt != row[i]:
                passes_filters = False
                break

        if passes_filters:
            result.append(row)

    f.close()

    return result

if __name__ == '__main__':
    clear()
    print("Part 1 of demo: correctness.")
    print("Given a small special value chosen live, 3 small CSV's of integers will be generated where that value shows up with controlled frequency.")
    prompt()
    print('''For each CSV we'll print...
    - number of rows, columns, and positive rows
    - contents of the CSV
    - our results (rows returned by filter), using our CSV parser written in C and using raw filters.
    ''')
    
    val = get_input_in_range(0, 9)
    for i in [0, 1, 3]:
        clear()
        print(f"Special value is {val}")
        print(f"Filtering on the 1st column")
        print(f"Number of rows is 8")
        print(f"Number of cols is 8")
        print(f"Number of positive rows is {i}")
        fname = make_small_demo_csv(num_positive=i, special_value=val)

        prompt()

        sievecsvfiltered = SieveCSV.parse_csv(fname, [0], [str(val)])

        print(f"Our parser, using SIMD, returns {len(sievecsvfiltered)} rows")
        print(f"... which are the following: ")

        for row in sievecsvfiltered:
            print(f"\t{row}")
        prompt()
    clear()

    print("Part 2 of demo: performance.")
    print("Given larger value chosen live, 3 large CSV's of integers will be generated")
    print("where that value shows up with controlled frequency.")
    print('''For each CSV we'll print...
    - number of rows, columns, and positive rows
    - first few rows of CSV
    - for the CSV parser we wrote, for both the case that the raw filters are used and the case that they aren't
    -- some of the rows returned by the parser
    -- number of correct and incorrect rows returned by the parser
    -- time taken by the parser, median over 250 runs.
    ''')
    val = get_input_in_range(1000, 9999)

    times = dict()
    sels = [0.1, 0.01, 0.001, 0.0001, 0.0]
    for sel in sels:
        prompt()
        clear()
        print(f"Special value is {val}")
        print(f"Filtering on the 1st column")
        print(f"Number of rows is 10000")
        print(f"Expected number of cols is 8")
        print(f"Expected selectivity is {sel}")
        fname, pos_rows = make_large_demo_csv(frac_positive=sel, special_value=val)

        correct_rows = filter_csv(fname, cols=[0], filters=[str(val)])
        prompt()

        no_raw_sievecsvfiltered = None  
        no_raw_times = list()
        for i in range(250): 
            no_raw_csv_start = time.time_ns()
            no_raw_sievecsvfiltered = SieveCSV.parse_csv(fname, [0], [str(val)], simd_mode=3)
            no_raw_csv_end = time.time_ns()
            no_raw_times.append(no_raw_csv_end - no_raw_csv_start)
        no_raw_times.sort()
        
        no_raw_time_avg = 0.5 * (no_raw_times[124] + no_raw_times[125])
        print(f"Our parser, without using raw filters, returns the following rows (and maybe other rows as well): ")
        i = 0
        for row in no_raw_sievecsvfiltered:
            print(f"\t{row}")
            i += 1
            if i == 3:
                break
        no_raw_correct = 0
        no_raw_wrong = 0
        no_raw_missing = 0
        for row in no_raw_sievecsvfiltered:
            if row in correct_rows:
                no_raw_correct += 1
            else:
                no_raw_wrong += 1
        print(f"Our parser, not using raw filters, returns {no_raw_correct} correct rows, {no_raw_wrong} wrong rows, and is missing {no_raw_missing} rows.")
        print(f"Our parser, not using raw filters, takes {round((no_raw_time_avg) / 10**6, 4)} ms.")
        
        prompt()

        raw_sievecsvfiltered = None
        raw_times = list()
        for i in range(250): # running multiple times, to control for caching
            raw_csv_start = time.time_ns()
            raw_sievecsvfiltered = SieveCSV.parse_csv(fname, [0], [str(val)])
            raw_csv_end = time.time_ns()
            raw_times.append(raw_csv_end - raw_csv_start)
        raw_times.sort()
        raw_time_avg = 0.5 * (raw_times[124] + raw_times[125])
        print(f"Our parser, using raw filters, returns the following rows (and maybe other rows as well): ")
        i = 0
        for row in raw_sievecsvfiltered:
            print(f"\t{row}")
            i += 1
            if i == 3:
                break
        
        for row in correct_rows:
            if row not in no_raw_sievecsvfiltered:
                no_raw_missing += 1

        raw_correct = 0
        raw_wrong = 0
        raw_missing = 0
        for row in raw_sievecsvfiltered:
            if row in correct_rows:
                raw_correct += 1
            else:
                raw_wrong += 1

        for row in correct_rows:
            if row not in raw_sievecsvfiltered:
                raw_missing += 1

        print(f"Our parser, using raw filters, returns {raw_correct} correct rows, {raw_wrong} wrong rows, and is missing {raw_missing} rows.")
        print(f"Compared to without raw filters, which takes {round((no_raw_time_avg) / 10**6, 4)} ms, our parser, using raw filters, takes {round((raw_time_avg) / 10**6, 4)} ms. ")
        times[(sel, False)] = (no_raw_time_avg) / 10**6
        times[(sel, True)] = (raw_time_avg) / 10**6
    prompt()
    clear()
    print("Timings summary, in ms")
    print(f"{'Selectivity'.ljust(12, ' ')}|{'no filter'.ljust(9)}|{'filter'.ljust(9)}|")
    print("=" * 33)
    for i in sels:
        sel_col = f"{i}".ljust(12, " ")
        no_fil_col = f"{round(times[(i, False)], 4)}".ljust(9, " ")
        fil_col = f"{round(times[(i, True)], 4)}".ljust(9, " ")
        print(f"{sel_col}|{no_fil_col}|{fil_col}|")
    _ = input("[end]")
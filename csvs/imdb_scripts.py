import csv


def trim_title():
    N = 1000
    fin = open('title.basics.csv', 'r')
    cr = csv.reader(fin, delimiter=',')

    shortened = []
    for i in range(0, N):
        shortened.append(cr.__next__())

    fout = open('title.basics.short.csv', 'w')
    cw = csv.writer(fout, lineterminator="\n")
    cw.writerows(shortened)

def convert_tsv_to_csv():
    with open('title.basics.tsv','r') as fin:
        with open('title.basics.csv','w', newline='') as fou:
            cr = csv.reader(fin, delimiter='\t')
            cw = csv.writer(fou, lineterminator="\n")
            count = 0
            count_p = 0
            for line in cr:
                incl = True
                count_p += 1
                for i in line:
                    if len(i) > 64:
                        count += 1
                        incl = False
                        break
                if incl:
                    cw.writerow(line)
            print(count, count_p)

def main():
    convert_tsv_to_csv()
    # trim_title()

if __name__ == '__main__':
    main()

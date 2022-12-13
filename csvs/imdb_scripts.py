import csv


def trim_title():
    N = 1000
    fin = open('title.basics.csv', 'r')
    cr = csv.reader(fin, delimiter=',')

    shortened = []
    for i in range(0, N):
        shortened.append(cr.__next__())

    fout = open('title.basics.short.csv', 'w')
    cw = csv.writer(fout, quotechar='', quoting=csv.QUOTE_NONE)
    cw.writerows(shortened)


def convert_tsv_to_csv():
    with open('title.basics.csv','r') as fin:
        cr = csv.reader(fin, delimiter=',')
        filecontents = [line for line in cr]

    with open('title.basics.csv','w') as fou:
        cw = csv.writer(fou, quotechar='', quoting=csv.QUOTE_NONE, escapechar='\\')
        cw.writerows(filecontents)

def main():
    trim_title()

if __name__ == '__main__':
    main()

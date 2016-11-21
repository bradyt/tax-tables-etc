
import csv

def get_csv(csv_infile):
    with open(csv_infile, 'r') as f:
        reader = csv.reader(f)
        rows = []
        for row in reader:
            ints = list(map(int, row))
            rows.append(ints)
        return rows

rows = get_csv('csvs/tax-table-2016.csv')

pairs = []

for pair in list(zip(rows, rows[1:])):
    pairs.append(pair)

# add an assertion for start, end = $0, $1,000,000

def pair_assertions(pair):
    curr, next = pair
    if curr[1] == next[0] and 0.25 * curr[1] > max(curr[2:]):
        return True
    else:
        print('error at ' + str(pair))
        return False

def all_pairs_pass(pairs):
    return all(map(pair_assertions, pairs))

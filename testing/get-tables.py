import re

with open('tax-tables-to-parse.txt', 'r') as f:
    read_data = f.read()
f.closed

pages = read_data.split('\u000c') # split on ^L

prototype_page = pages[1]

# print(prototype_page)

lines = prototype_page.splitlines()

def get_column_delimiters(line):
    column_delimiters = []
    for column in range(len(line)):
        if line.startswith("If line 43", column):
            column_delimiters.append(column)
    return column_delimiters

for line in lines:
    if line[:].startswith("If line 43"):
        column_delimiters = get_column_delimiters(line)

def get_rows(lines):
    def line_is_numbers(line):
        return re.match("^[0-9 ,]+$", line)
    filtered_lines = []
    for i in range(len(lines)):
        if lines[i].startswith("At"):
            for j in range(i, len(lines)):
                if line_is_numbers(lines[j]):
                    filtered_lines.append(lines[j])
    return filtered_lines

rows = get_rows(lines)

matrix = []
for row in rows:
    start = column_delimiters
    end = column_delimiters[1:]
    end.append(len(row))
    matrix_row = []
    for i, j in zip(start, end):
        matrix_row.append(row[i:j])
    matrix.append(matrix_row)

def flatten_matrix_downward(matrix):
    width = len(matrix[0])
    height = len(matrix)
    flattened = []
    for i in range(width):
       for j in range(height):
           flattened.append(matrix[j][i])
    return flattened

flattened = flatten_matrix_downward(matrix)

def strip_blank_lines(lines):
    stripped_lines = []
    for line in lines:
        if not re.match("^ *$", line):
            stripped_lines.append(line)
    return stripped_lines

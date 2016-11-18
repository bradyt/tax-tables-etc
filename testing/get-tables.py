
import re
from pprint import pprint

import csv

#    ______     __     __        __    __
#   / ____/__  / /_   / /_____ _/ /_  / /__  _____
#  / / __/ _ \/ __/  / __/ __ `/ __ \/ / _ \/ ___/
# / /_/ /  __/ /_   / /_/ /_/ / /_/ / /  __(__  )
# \____/\___/\__/   \__/\__,_/_.___/_/\___/____/

class Page(object):

    def __init__(self, page):
        self.lines = page.splitlines()
        self._43_line_number = None
        self._43_line = None
        self._43_column_numbers = []
        self.table_lines = []
        self.tables = []
        self.get_43_line_number()
        self.get_43_line()
        self.get_43_column_numbers()
        self.get_table_lines()
        self.get_tables()

    def get_43_line_number(self):
        for line_number, line in enumerate(self.lines):
            if line.startswith("If line 43"):
                self._43_line_number = line_number
                break

    def get_43_line(self):
        self._43_line = self.lines[self._43_line_number]

    def get_43_column_numbers(self):
        for position in range(len(self._43_line)):
            if self._43_line.startswith("If line 43", position):
                self._43_column_numbers.append(position)

    def get_table_lines(self):
        def split_at_edges(line, edges):
            return [line[i:j] for i, j in zip(edges, edges[1:] + [None])]
        for line in self.lines:
            self.table_lines.append(
                split_at_edges(line, self._43_column_numbers))

    def get_tables(self):
        self.tables = list(map(Table, transpose(self.table_lines)))

    # pagelines  tablelines    tables
    # [abc,      [[a, b, c],   [[a, d]
    #  def]       [d, e, f]]    [b, e]
    #                           [c, f]]

def transpose(matrix):
    return list(map(list, zip(*matrix)))

#    ______     __               ____
#   / ____/__  / /_   ________  / / /____
#  / / __/ _ \/ __/  / ___/ _ \/ / / ___/
# / /_/ /  __/ /_   / /__/  __/ / (__  )
# \____/\___/\__/   \___/\___/_/_/____/

class Table(object):
    def __init__(self, table_lines):
        self.table_lines = table_lines
        self.At_line_number = None
        self.header_row = None
        self.uppercase_column_numbers = []
        self.table_of_lines_of_cells = []
        self.get_At_line_number()
        self.get_header_row()
        self.get_uppercase_column_numbers()
        self.split_to_cells()
        self.filter_for_cells()
        self.clean_remaining_cells()

    def get_At_line_number(self):
        for line_number, line in enumerate(self.table_lines):
            if line.startswith("At"):
                self.At_line_number = line_number

    def get_header_row(self):
        self.header_row = self.table_lines[self.At_line_number]
        
    def get_uppercase_column_numbers(self):
        for position, char in enumerate(self.header_row):
            if char.isupper():
                self.uppercase_column_numbers.append(position)

    def split_to_cells(self):
        def split_at_edges(line, edges):
            return [line[i:j] for i, j in zip(edges, edges[1:] + [None])]
        for line in self.table_lines:
            current_line_of_cells = []
            for cell in split_at_edges(line, self.uppercase_column_numbers):
                current_line_of_cells.append(cell)
            self.table_of_lines_of_cells.append(current_line_of_cells)

    def filter_for_cells(self):
        def cells_are_cells(list_of_cells):
            def cell_is_cell(cell):
                return re.search("([0-9]+,)*[0-9]+", cell)
            return all(map(cell_is_cell, list_of_cells))
        result = []
        for list_of_cells in self.table_of_lines_of_cells:
            if cells_are_cells(list_of_cells):
                result.append(list_of_cells)
        self.table_of_lines_of_cells = result

    def clean_remaining_cells(self):
        def clean(cell):
            return cell.replace(" ", "").replace(",", "")
        new_table = []
        for line_of_cells in self.table_of_lines_of_cells:
            new_line = []
            for cell in line_of_cells:
                new_line.append(clean(cell))
            new_table.append(new_line)
        self.table_of_lines_of_cells = new_table

#    ______     __
#   / ____/__  / /_   ____  ____ _____ ____  _____
#  / / __/ _ \/ __/  / __ \/ __ `/ __ `/ _ \/ ___/
# / /_/ /  __/ /_   / /_/ / /_/ / /_/ /  __(__  )
# \____/\___/\__/  / .___/\__,_/\__, /\___/____/
#                 /_/          /____/

def file_to_list_of_page(file):
    pages = file.split('\u000c') # split on ^L
    pages_with_43 = []
    for page in pages:
        for line in page.splitlines():
            if line.startswith("If line 43"):
                pages_with_43.append(page)
                break
    return pages_with_43

#     ____           __  __            ____
#    / __ \____     / /_/ /_  ___     / __ \___ _      __
#   / / / / __ \   / __/ __ \/ _ \   / / / / _ \ | /| / /
#  / /_/ / /_/ /  / /_/ / / /  __/  / /_/ /  __/ |/ |/ /
# /_____/\____/   \__/_/ /_/\___/  /_____/\___/|__/|__/

def main():
    with open('tax-tables-to-parse.txt', 'r') as f:
        read_data = f.read()
    f.closed
    
    pages = file_to_list_of_page(read_data)
    with open("output.csv", "w") as f:
        writer = csv.writer(f)
        for page in pages:
            page_object = Page(page)
            for table_object in page_object.tables:
                for line_of_cells in table_object.table_of_lines_of_cells:
                    # pprint(line_of_cells)
                        writer.writerow(line_of_cells)
            

    # page = Page(pages[2])
    
    # table = page.tables[0]

if __name__ == '__main__':
    main()

# from pprint import pprint
# with open('tax-tables-to-parse.txt', 'r') as f:
#     read_data = f.read()
# f.closed

# pages = get_pages_with_43(read_data)

# pages_of_tables = []
# for page in pages:
#     page_lines = page.splitlines()
#     tables = chop_horizontally_to_43_and_transpose(page_lines)
#     pages_of_tables.append(tables)

# def main():
#     pprint(pages_of_tables, width=1000)

# # prototype_page = pages[0]

# # page_lines = prototype_page.splitlines()

# # tables = chop_horizontally_to_If_line_43_and_transpose(page_lines)

# # table = tables[0]

# # prototype_table = try_evolving_output(prototype_page)[0]
# # trimmed_prototype_table = trim_to_At_line_number(prototype_table)
# # uppercase_column_numbers = get_uppercase_column_numbers(trimmed_prototype_table[0])

# # def trim_to_numbers(lines):
# #     for line_number, line in enumerate(lines):
# #        if re.match("^ *([0-9,]+ +){5}[0-9]+ *$", line):
# #            return lines[line_number:]

# # trimmed_again_prototype_table = trim_to_numbers(trimmed_prototype_table)

# # def split_lines_on_columns(sub_table):
# #     pass

# # def get_bottom_line_number(lines):
# #     for line_number, line in reversed(list(enumerate(lines))):
# #         if re.match("^[0-9 ,]+$", line):
# #             return line_number

# # def trim_to_top_and_bottom_lines(lines):
# #     for line_number, line in enumerate(lines):
# #         if line.startswith("If line 43"):
# #             top = line_number
# #             break
# #     for line_number, line in reversed(list(enumerate(lines))):
# #         if re.match("^[0-9 ,]+$", line):
# #             bottom = line_number
# #             break
# #     return lines[top:bottom + 1]

# # def try_evolving_output(page):
# #     lines = page.splitlines()
# #     lines = trim_to_top_and_bottom_lines(lines)
# #     edges = get_table_edges(lines[0])
# #     matrix = split_lines_at_edges(lines, edges)
# #     sub_tables = get_sub_tables(matrix)
# #     return sub_tables

# # def trim_to_At_line_number(lines):
# #     for line_number, line in enumerate(lines):
# #         if line.startswith("At"):
# #             return lines[line_number:]

#    __  __                          __
#   / / / /___  __  __________  ____/ /
#  / / / / __ \/ / / / ___/ _ \/ __  /
# / /_/ / / / / /_/ (__  )  __/ /_/ /
# \____/_/ /_/\__,_/____/\___/\__,_/

# def get_uppercase_column_numbers(table_lines):
#     uppercase_column_numbers = []
#     At_line_number = get_At_line_number(table_lines)
#     header_row = table_lines[At_line_number]
#     for position, char in enumerate(header_row):
#         if char.isupper():
#             uppercase_column_numbers.append(position)
#     return uppercase_column_numbers

# def get_table_cells(table_lines):
#     edges = get_uppercase_column_numbers(table_lines)
#     def split_at_edges(line):
#         return [ line[i:j] for i, j in zip(edges, edges[1:] + [None]) ]
#     table_cells = map(split_at_edges, table_lines)
#     return table_cells

# # def get_rows(lines):
# #     filtered_lines = []
# #     for i in range(len(lines)):
# #         if lines[i].startswith("At"):
# #             for j in range(i, len(lines)):
# #                 if line_is_numbers(lines[j]):
# #                     filtered_lines.append(lines[j])
# #     return filtered_lines

# # rows = get_rows(lines)

# # matrix = []
# # for row in rows:
# #     start = table_edges
# #     end = table_edges[1:]
# #     end.append(len(row))
# #     matrix_row = []
# #     for i, j in zip(start, end):
# #         matrix_row.append(row[i:j])
# #     matrix.append(matrix_row)

# # def flatten_matrix_downward(matrix):
# #     width = len(matrix[0])
# #     height = len(matrix)
# #     flattened = []
# #     for i in range(width):
# #        for j in range(height):
# #            flattened.append(matrix[j][i])
# #     return flattened

# # flattened = flatten_matrix_downward(matrix)

# # def strip_blank_lines(lines):
# #     stripped_lines = []
# #     for line in lines:
# #         if not re.match("^ *$", line):
# #             stripped_lines.append(line)
# #     return stripped_lines

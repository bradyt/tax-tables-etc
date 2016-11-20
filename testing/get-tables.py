
import os
import re
from pprint import pprint
import csv 
import xml.etree.ElementTree as ET

os.chdir(os.path.expanduser("~/my-tax-tools/testing"))

def write_rows_to_file(rows, outfile):
    with open(outfile, "w") as f:
        writer = csv.writer(f)
        for line in rows:
            writer.writerow(line)


def main():
    xml_filename = 'i1040gi--2014.xml'
    outline, pages = split_tree(xml_filename)
    page_numbers = get_page_numbers(outline)
    tax_table_pages = get_pages(pages, page_numbers)
    list_ = get_list(tax_table_pages)
    rows = get_rows(list_)
    # return rows
    write_rows_to_file(rows, 'output.csv')

def split_tree(xml_filename):
    tree = ET.parse(xml_filename)
    root = tree.getroot()
    outline = root.find('outline').getchildren()
    pages = root.findall('page')
    return outline, pages

def get_page_numbers(outline):
    start, end = None, None
    for item in outline:
        if item.text == '2014 Tax Table':
            start = int(item.attrib['page'])
        if item.text == 'General Information':
            end = int(item.attrib['page']) - 1
    return start, end

def get_pages(pages, page_numbers):
    start, end = page_numbers
    tax_table_pages = []
    for page in pages:
        page_number = int(page.attrib['number'])
        if page_number in range(start, end):
           tax_table_pages.append(page) 
    return tax_table_pages

def get_list(pages):
    list_ = []
    for page in pages:
        for item in page:
            if int(item.attrib['font']) in [11, 12]:
                string = ''.join(item.itertext())
                string = re.sub(r'[^0-9^ ]', '', string)
                list_ += map(int, string.split())
    return list_

def get_rows(ls):
    rows = []
    i = 0
    while True:
        row = ls[i:i + 6]
        if not row:
            break
        if len(row) == 6:
            print(row)
            rows.append(row)
        i += 6
    # while i + 4 < len(ls):
    #     print(i)
    #     if ls[i + 1] - ls[i] % 50 == 0 or ls[i] < 20:
    #         less = True
    #         for j in range(4):
    #             if ls[i + 2 + j] > 0.2 * ls[i]:
    #                 less = False
    #         if less:
    #             row = [ls[i + j] for j in range(6)]
    #             print(row)
    #             rows.append(row)
    #             i += 6
    #     else:
    #         i += 1
    return rows

# def get_line_43_indices(page):
#     indices = []
#     for i in range(len(page)):
#         if page[i].text == None:
#             if ''.join(page[i].itertext()) == "If line 43":
#                 indices.append(i)
#     indices.append(len(page))
#     return list(zip(indices, indices[1:]))

# def add_rows_to_list(page, list):
#     row = []
#     i = 0
#     for item in page:
#         if int(item.attrib['font']) in [11, 12]:
#             string = ''.join(page[i].itertext())
#             string = re.sub(r'[^0-9^ ]', '', string)
#             row += map(int, string.split())
#     while len(row) < 6:
#         row.append(2 * 10 ** 6)
#     list.append(row)
#     return list

# def add_numbers_to_list(page, indices, list):
#     for start, end in indices:
#         for i in range(start, end - 1):
#             if int(page[i].attrib['font']) in [11, 12]:
#                 string = ''.join(page[i].itertext())
#                 string = re.sub(r'[^0-9^ ]', '', string)
#                 list += map(int, string.split())
#     return list

# def turn_list_to_rows(list):
#     i = 0
#     rows = []
#     while i + 5 < len(list):
#         next = judge_starting_position(i, list)
#         if next:
#             rows.append(next)
#         else:
#             i += 1
#     return rows

# def judge_starting_position(i, list):
#     next = [ list[i + j] for j in range(6) ]
#     if next[1] == next[0] + 25 and all(
#             map(lambda j: next[j] < .2 * next[0],
#                 range(6))):
#         return next
#     else:
#         return None

# def extract_csv_tax_table_from_txt(txt_infile, csv_outfile):
#     with open(txt_infile, 'r') as f:
#         read_data = f.read()

#     book = Book(read_data)

#     pages = file_to_list_of_page(read_data)
#     with open(csv_outfile, "w") as f:
#         writer = csv.writer(f)
#         for page_object in book.page_objects:
#             for table_object in page_object.tables:
#                 for line_of_cells in table_object.table_of_lines_of_cells:
#                     # pprint(line_of_cells)
#                     writer.writerow(line_of_cells)

if __name__ == '__main__':
    main()

# def xml_in_csv_out(infile, outfile):
#     tree = ET.parse(infile)
#     csvlist = make_csv_list_from_xml_tree(tree)
#     csvrows = list_to_rows(csvlist)
#     with open(outfile, "w") as f:
#         writer = csv.writer(f)
#         for line in csvrows:
#             writer.writerow(line)

# This function takes an XML Tax Table tree and returns a CSV in list
# form.
            
# def make_csv_list_from_xml_tree(tree):
#     root = tree.getroot()
#     start, end = get_range_of_tax_table_pages(root)
#     tax_table_pages = get_tax_table_pages(root, start, end)
#     list_of_numbers = []
#     for page in tax_table_pages:
#         indices = get_line_43_indices(page)
#         list_of_numbers = add_numbers_to_list(page, indices, list_of_numbers)
#     return list_of_numbers

#    ______     __
#   / ____/__  / /_   ____  ____ _____ ____  _____
#  / / __/ _ \/ __/  / __ \/ __ `/ __ `/ _ \/ ___/
# / /_/ /  __/ /_   / /_/ / /_/ / /_/ /  __(__  )
# \____/\___/\__/  / .___/\__,_/\__, /\___/____/
#                 /_/          /____/

# class Book(object):

#     def __init__(self, filename):
#         self.filename = filename
#         self.file_string = None
#         self.pages = []
#         self.page_objects = []
#         self.update_file_string()
#         self.update_pages()
#         # self.update_page_objects()

#     def update_file_string(self):
#         with open(self.filename, 'r') as f:
#             self.file_string = f.read()
    
#     def update_pages(self):
#         for page in self.file_string.split('\f'):
#             for line in page.splitlines():
#                 if line.startswith("If line 43"):
#                     self.pages.append(page)
#                     break

#     def update_page_objects(self):
#         for page in self.pages:
#             self.pages.append(Page(page))

# #    ______     __     __        __    __
# #   / ____/__  / /_   / /_____ _/ /_  / /__  _____
# #  / / __/ _ \/ __/  / __/ __ `/ __ \/ / _ \/ ___/
# # / /_/ /  __/ /_   / /_/ /_/ / /_/ / /  __(__  )
# # \____/\___/\__/   \__/\__,_/_.___/_/\___/____/

# class Page(object):

#     def __init__(self, page):
#         self.lines = page.splitlines()
#         self._43_line_number = None
#         self._43_line = None
#         self._43_column_numbers = []
#         self.table_lines = []
#         self.tables = []
#         self.table_objects = []
#         self.update_43_line_and_number()
#         self.update_43_column_numbers()
#         self.update_table_lines()
#         self.update_tables()

#     def update_43_line_and_number(self):
#         for line_number, line in enumerate(self.lines):
#             if line.startswith("If line 43"):
#                 self._43_line_number = line_number
#                 self._43_line = line
#                 break

#     def update_43_column_numbers(self):
#         for position in range(len(self._43_line)):
#             if self._43_line.startswith("If line 43", position):
#                 self._43_column_numbers.append(position)

#     def update_table_lines(self):
#         def split_at_edges(line, edges):
#             return [line[i:j] for i, j in zip(edges, edges[1:] + [None])]
#         for line in self.lines:
#             self.table_lines.append(
#                 split_at_edges(line, self._43_column_numbers))

#     def update_tables(self):
#         self.tables = list(transpose(self.table_lines))

#     def update_table_objects(self):
#         self.table_objects = list(map(Table, self.tables))

#     # pagelines  tablelines    tables
#     # [abc,      [[a, b, c],   [[a, d]
#     #  def]       [d, e, f]]    [b, e]
#     #                           [c, f]]

# # def transpose(matrix):
# #     return list(map(list, zip(*matrix)))

# book = Book('tax-tables-to-parse.txt')
# page0 = book.pages[0]
# page1 = book.pages[1]
# pagen = book.pages[-1]
# # pages = book.pages
# # page = pages[0]

# page0_object = Page(page0)
# pagen_object = Page(pagen)

# table00 = page0_object.tables[0]
# tablenm = pagen_object.tables[-2]
# tablenn = pagen_object.tables[-1]

# #    ______     __               ____
# #   / ____/__  / /_   ________  / / /____
# #  / / __/ _ \/ __/  / ___/ _ \/ / / ___/
# # / /_/ /  __/ /_   / /__/  __/ / (__  )
# # \____/\___/\__/   \___/\___/_/_/____/

# class Table(object):
#     def __init__(self, table_lines):
#         self.table_lines = table_lines
#         self.At_line_number = None
#         self.header_row = None
#         self.uppercase_column_numbers = []
#         self.table_of_lines_of_cells = []
#         self.update_At_line_number()
#         self.update_header_row()
#         self.update_uppercase_column_numbers()
#         self.split_to_cells()
#         self.filter_for_cells()
#         self.clean_remaining_cells()

#     def update_At_line_number(self):
#         for line_number, line in enumerate(self.table_lines):
#             if line.startswith("At"):
#                 self.At_line_number = line_number

#     def update_header_row(self):
#         self.header_row = self.table_lines[self.At_line_number]
        
#     def update_uppercase_column_numbers(self):
#         for position, char in enumerate(self.header_row):
#             if char.isupper():
#                 self.uppercase_column_numbers.append(position)

#     def split_to_cells(self):
#         def split_at_edges(line, edges):
#             return [line[i:j] for i, j in zip(edges, edges[1:] + [None])]
#         for line in self.table_lines:
#             current_line_of_cells = []
#             for cell in split_at_edges(line, self.uppercase_column_numbers):
#                 current_line_of_cells.append(cell)
#             self.table_of_lines_of_cells.append(current_line_of_cells)

#     def filter_for_cells(self):
#         def cells_are_cells(list_of_cells):
#             def cell_is_cell(cell):
#                 return re.search("([0-9]+,)*[0-9]+", cell)
#             return all(map(cell_is_cell, list_of_cells))
#         result = []
#         for list_of_cells in self.table_of_lines_of_cells:
#             if cells_are_cells(list_of_cells):
#                 result.append(list_of_cells)
#         self.table_of_lines_of_cells = result

#     def clean_remaining_cells(self):
#         def clean(cell):
#             return cell.replace(" ", "").replace(",", "")
#         new_table = []
#         for line_of_cells in self.table_of_lines_of_cells:
#             new_line = []
#             for cell in line_of_cells:
#                 new_line.append(clean(cell))
#             new_table.append(new_line)
#         self.table_of_lines_of_cells = new_table

# # #     ____           __  __            ____
# # #    / __ \____     / /_/ /_  ___     / __ \___ _      __
# # #   / / / / __ \   / __/ __ \/ _ \   / / / / _ \ | /| / /
# # #  / /_/ / /_/ /  / /_/ / / /  __/  / /_/ /  __/ |/ |/ /
# # # /_____/\____/   \__/_/ /_/\___/  /_____/\___/|__/|__/

# # def main():
# #     extract_csv_tax_table_from_txt(
# #         'testing/tax-tables-to-parse.txt',
# #         "testing/output.csv")

# # def extract_csv_tax_table_from_txt(txt_infile, csv_outfile):
# #     with open(txt_infile, 'r') as f:
# #         read_data = f.read()

# #     book = Book(read_data)

# #     pages = file_to_list_of_page(read_data)
# #     with open(csv_outfile, "w") as f:
# #         writer = csv.writer(f)
# #         for page_object in book.page_objects:
# #             for table_object in page_object.tables:
# #                 for line_of_cells in table_object.table_of_lines_of_cells:
# #                     # pprint(line_of_cells)
# #                     writer.writerow(line_of_cells)

# # if __name__ == '__main__':
# #     main()

# #    __  __                          __
# #   / / / /___  __  __________  ____/ /
# #  / / / / __ \/ / / / ___/ _ \/ __  /
# # / /_/ / / / / /_/ (__  )  __/ /_/ /
# # \____/_/ /_/\__,_/____/\___/\__,_/

# # def trim_to_numbers(lines):
# #     for line_number, line in enumerate(lines):
# #        if re.match("^ *([0-9,]+ +){5}[0-9]+ *$", line):
# #            return lines[line_number:]

# # def update_bottom_line_number(lines):
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

# # def trim_to_At_line_number(lines):
# #     for line_number, line in enumerate(lines):
# #         if line.startswith("At"):
# #             return lines[line_number:]

# # def update_uppercase_column_numbers(table_lines):
# #     uppercase_column_numbers = []
# #     At_line_number = update_At_line_number(table_lines)
# #     header_row = table_lines[At_line_number]
# #     for position, char in enumerate(header_row):
# #         if char.isupper():
# #             uppercase_column_numbers.append(position)
# #     return uppercase_column_numbers

# # def update_table_cells(table_lines):
# #     edges = update_uppercase_column_numbers(table_lines)
# #     def split_at_edges(line):
# #         return [ line[i:j] for i, j in zip(edges, edges[1:] + [None]) ]
# #     table_cells = map(split_at_edges, table_lines)
# #     return table_cells

# # def update_rows(lines):
# #     filtered_lines = []
# #     for i in range(len(lines)):
# #         if lines[i].startswith("At"):
# #             for j in range(i, len(lines)):
# #                 if line_is_numbers(lines[j]):
# #                     filtered_lines.append(lines[j])
# #     return filtered_lines

# # rows = update_rows(lines)

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


import os
import re
from pprint import pprint
import csv 
import xml.etree.ElementTree as ET

def write_rows_to_file(rows, outfile):
    with open(outfile, "w") as f:
        writer = csv.writer(f)
        for line in rows:
            writer.writerow(line)

def xml_to_csv(xml_infile, csv_outfile):
    all_pages = get_all_pages(xml_infile)
    tax_table_pages = get_tax_table_pages(all_pages)
    list_ = get_list(tax_table_pages)
    rows = get_rows(list_)
    write_rows_to_file(rows, csv_outfile)

def get_all_pages(xml_filename):
    tree = ET.parse(xml_filename)
    root = tree.getroot()
    pages = root.findall('page')
    return pages

def get_tax_table_pages(pages):
    tax_table_pages = []
    for page in pages:
        tax_table = False
        for item in page:
            if 'If line 43' in ''.join(item.itertext()):
                tax_table = True
        if tax_table:
            tax_table_pages.append(page)
    return tax_table_pages

def get_list(pages):
    list_ = []
    for page in pages:
        for item in page:
            if item.get('font') in ['11', '12']:
                string = ''.join(item.itertext())
                string = re.sub(r'[^0-9^ ]', '', string)
                list_ += map(int, string.split())
    return list_

def get_rows(list_):
    rows = []
    i = 0
    # for i in range(0, len(list_), 6):
    while True:
        row = list_[i:i + 6]
        if not row:
            break
        if len(row) == 6:
            rows.append(row)
        i += 6
    return rows

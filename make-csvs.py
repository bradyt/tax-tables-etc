
import re
import glob, os

import get_tables

def get_csv_filename(infile):
    base = re.sub(".*--([0-9]{4}).xml", "\\1", infile)
    return 'csvs/tax-table-' + base + '.csv'

xml_files = [
    # 'xmls/i1040gi--2013.xml',
    # 'xmls/i1040gi--2014.xml',
    'xmls/i1040gi--2015.xml'
]

for infile in xml_files:
    outfile = get_csv_filename(infile)
    print('Reading ' + infile + '...')
    get_tables.xml_to_csv(infile, outfile)
    print('Wrote to ' + outfile)

print('Done!')
    

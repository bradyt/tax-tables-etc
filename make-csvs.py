
import re
import glob, os
os.chdir(os.path.expanduser("~/my-tax-tools"))

import get_tables

for infile in glob.glob("xmls/*.xml"):
    print(infile)
    # base = re.sub(".*--([0-9]{4}).xml", "\\1", infile)
    # outfile = 'csvs/tax-table-' + base + '.csv'
    # print('Reading $infile...')
    # get_tables.xml_to_csv(infile, outfile)
    # print('Wrote to $outfile')

print('Done!')

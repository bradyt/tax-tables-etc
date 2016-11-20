
import re
import glob, os
os.chdir(os.path.expanduser("~/my-tax-tools"))

for infile in glob.glob("txts/*.txt"):
    base = re.sub(".*--([0-9]{4}).txt", "\\1", infile)
    outfile = 'csvs/tax-table-' + base + '.csv'
    print(infile)
    print(outfile)
    

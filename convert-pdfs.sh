for infile in pdfs/*.pdf
do
    echo "converting $infile..."
    outfile=xmls/$(basename $infile .pdf).xml
    pdftohtml -xml -i $infile $outfile
done
echo "done"

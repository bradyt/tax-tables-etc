for infile in pdfs/*.pdf
do
    outfile=txts/$(basename $infile .pdf).txt
    pdftotext -layout $infile $outfile
done

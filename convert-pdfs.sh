for infile in pdfs/*.pdf
do
    echo "converting $infile..."
    outfile=txts/$(basename $infile .pdf).txt
    pdftotext -layout $infile $outfile
done
echo "done"

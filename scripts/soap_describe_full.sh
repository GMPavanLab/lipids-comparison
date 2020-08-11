for cut in 20 30
do
   python soap_describe.py -s phosphate -c $cut -a False -ow True
   python soap_describe.py -s 4beads -c $cut -a False -ow True
done

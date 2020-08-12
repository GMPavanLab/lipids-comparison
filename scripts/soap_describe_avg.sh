#!/bin/bash
for cut in 11 15 20 30 40
do
   python soap_describe.py -s phosphate -c $cut -a inner -ow True
   python soap_describe.py -s 4beads -c $cut -a inner -ow True
done

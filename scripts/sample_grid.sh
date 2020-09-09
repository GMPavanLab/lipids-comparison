#!/bin/bash
for cut in 20 30
do
   python sample_grid.py -s phosphate -c $cut -z 50000
   python sample_grid.py -s 4beads -c $cut -z 50000 
done

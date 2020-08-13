#!/bin/bash
for cut in 11 15 20 30 40
do
   python distance_metric_avg.py -s phosphate -c $cut -ow True
   python distance_metric_avg.py -s 4beads -c $cut -ow True
done

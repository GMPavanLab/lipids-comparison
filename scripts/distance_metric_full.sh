#!/bin/bash
for cut in 30
do
   python distance_metric_full.py -s phosphate -c $cut -z 2000 -ow True
   python distance_metric_full.py -s 4beads -c $cut -z 2000 -ow True
done

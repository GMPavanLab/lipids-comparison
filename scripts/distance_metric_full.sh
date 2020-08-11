for cut in 20 30
do
   python distance_metric_full.py -s phosphate -c $cut -z 5000
   python distance_metric_full.py -s 4beads -c $cut -z 5000
done

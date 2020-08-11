for cut in 30 20
do
   python pca_full.py -s phosphate -c $cut -z 20000
   python pca_full.py -s 4beads -c $cut -z 20000
done

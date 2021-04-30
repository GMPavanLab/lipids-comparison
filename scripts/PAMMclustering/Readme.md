# PAMM density based clustering

**DISCLAIMER**
We do not have developed the original PAMM algorithm.
The original PAMM algorithm can be accessed online at [PAMM](https://github.com/cosmo-epfl/pamm) which is the implementation discussed in the original reference [PAMMreference](https://pubs.acs.org/doi/10.1021/acs.jctc.7b00993) (also avaliable there as SI files).

The notebook `pamm_clustering_general.ipynb` contains a general application of the PAMM clustering algorithm to a set of lipids membranes of different temperatures.

Following the original implementation this woud be the same as running the command:

`$PATH:$PWD/bin/pamm -d 5 -ngrid 2000 -qs 1.0 -fspred 0.3 -merger 0.001 -v -savegrid < all_bylayers.pca`

This would give as output the micro clusters that can be statistically analyzed to give the structural motifs (routine avaliable in the original implementation in the `/tools/merge.py` script).
Following the original implementation this can be done as

`python2.7 ../../tools/merge 2 PAMMoutput.grid PAMMoutput.bs`
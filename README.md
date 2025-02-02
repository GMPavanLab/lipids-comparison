This repository contains the code and procedures used for the paper "A Data-Driven Dimensionality Reduction Approach to Compare and Classify Lipid Force Fields". 

All the data needed to run the scripts and get the results presented in the paper can be either generated (starting from the input files in `simulations` folder) or downloaded from a Zenodo repository via the script in the root folder `download.sh`.


## Content
Data are organized in 3 different folders:

* `paper/`: Here we put scripts and images with the paper figures, inside this folder we have 2 subfolders:
   * `figures/`: Here we have the .png files with the article figures.
   * `plots/`: Here we have the GNUplot scripts and data for the single plots in fig 2.

* `simulations/`: Here we put all the input files needed to perform the gromacs simulations, divided by the kind of lipid analyzed
   * `input_files_DPPC/`: We have a folder for every FF analyzed (martini 2.2 and dry martini) for a DPPC lipid bilayer formed by 1152 lipid molecules. In these folders we have the _mdp_, _top_, and _conf_ subfolders with all the input files to perform the equilibration and production run for such system. 
   * `input_files_POPC/`: We have a folder for every FF analyzed (13 in total) for a POPC lipid bilayer formed by 128 lipid molecules. In these folders we have the _mdp_, _top_, and _conf_ subfolders with all the input files to perform the equilibration and production run for such system. 

* `scripts/`: it contains all the data manipulation scripts needed to perform our SOAP- and SOAP/PAMM-based calculations. Namely:
  * `soap_describe.py` computes SOAP spectra for POPC bilayers (the xyz can be obtained from the download script, see below).
  * `sample_grid.py` generates the grid to compute Jensen-Shannon distance matrix.
  * `distance_metric_avg.py` computes the SOAP distance matrix between the POPC FFs.
  * `distance_metric_full.py` computes the Jensen-Shanon distance matrix between the POPC FFs.
  * Inside the `PAMMCclustering` folder there is a jupyter notebook, _pamm_clustering_general.ipynb_ that computes the PAMM analysis starting from SOAP-PCA data.
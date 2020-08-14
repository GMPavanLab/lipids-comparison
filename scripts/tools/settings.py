import os

# Common settings

HOME = os.path.expanduser("~")
TR = "_1us"
MAX_TRAJ_SIZE = 4000

species = {
    "4beads": ["N", "P", "C"],
    "phosphate": ["P"]
}


# Settings for distance_metric_full.py

D_thr = 15  # Chisq parameter of PAk
F = 3  # this boy is just a trick to make the grid tighter around pdf
NEIGHBORS = 3  # number of neighbords to approximate density from PAk for oos estimations
PCA_DIMENSIONS = 5
SIZE = 50000  # size of dataset for PAk


# Settings for pca_full.py

FULL_ATOM = ['POPC_charmm36m_303K_PO4_NC3_C4A_C4B.npz', 
             'POPC_gromos43a1-s3_303K_PO4_NC3_C4A_C4B.npz',
             'POPC_lipid17_303K_PO4_NC3_C4A_C4B.npz',
             'POPC_slipids_303K_PO4_NC3_C4A_C4B.npz']
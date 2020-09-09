import glob
import time
import argparse

import numpy as np

from shared import *


D_thr = 15  # Chisq parameter of PAk
F = 3  # this boy is just a trick to make the grid tighter around pdf
NEIGHBORS = 3  # number of neighbords to approximate density from PAk for oos
PCA_DIMENSIONS = 5
IZE = 50000  # size of dataset for PAk


def main(system, cutoff, sample):

    prefix = "{}/Lipids/dscribe_{}{}/pca/{}_ang/".format(HOME, system, TR, cutoff)
    files = sorted(glob.glob("{}POPC_*npy".format(prefix)))

    files = [i for i in files if '303' in i]
    print('Processing {} trajectories at 303k'.format(len(files)))

    x = extract_sample(files, sample)

    x = np.hstack([x[:, :PCA_DIMENSIONS], x[:,-1:]])

    raw_grid = UniformGrid('minmax').fit(x[:, :-1]).transform(15)
    fine_grid = UniformGrid('minmax').fit(x[:, :-1]).lazy_transform(40, chunk=10000)
    print("Raw grid shape: {}".format(raw_grid.shape))
    raw_grid = np.hstack([raw_grid, np.zeros((raw_grid.shape[0], 1)) + np.max(x[:,-1]) + 1])
    knn = fit_grid_refiner(raw_grid, x)

    fine_grid = filter_grid(knn, fine_grid, 0.02)

    grid_filename = "{}/Lipids/dscribe_{}{}/grid_{}_ang".format(HOME, system, TR, cutoff)
    np.save(grid_filename, fine_grid)

    print("Filtered grid: {}".format(fine_grid.shape))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("-s", dest="system", type=str,
                        help="4beads or phospate file")

    parser.add_argument("-c", dest="cutoff", type=int,
                        help="config file")

    parser.add_argument("-z", dest="sample", type=int,
                        help="sample size")

    args = parser.parse_args()

    main(args.system, args.cutoff, args.sample)

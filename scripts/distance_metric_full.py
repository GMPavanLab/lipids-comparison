import glob
import time
import argparse

import numpy as np

from shared import *


D_thr = 15  # Chisq parameter of PAk
F = 3  # this boy is just a trick to make the grid tighter around pdf
NEIGHBORS = 3  # number of neighbords to approximate density from PAk for oos
SIZE = 50000  # size of dataset for PAk


def main(system, cutoff, sample, overwrite=True):

    prefix = "{}/Lipids/dscribe_{}{}/pca/{}_ang/".format(HOME, system, TR, cutoff)
    files = sorted(glob.glob("{}POPC_*npy".format(prefix)))

    print('Processing only 303k for now')
    files = [i for i in files if '303' in i]

    x = extract_sample(files, sample)

    x = np.hstack([x[:, :3], x[:,-1:]])

    raw_grid = UniformGrid('minmax').fit(x[:, :-1]).transform(25)
    fine_grid = UniformGrid('minmax').fit(x[:, :-1]).transform(100)
    print("Grid shapes: {}, {}".format(raw_grid.shape, fine_grid.shape))
    raw_grid = np.hstack([raw_grid, np.zeros((raw_grid.shape[0], 1)) + np.max(x[:,-1]) + 1])
    knn = filter_grid(raw_grid, x)

    v = knn.predict_proba(fine_grid)
    v[:,-1] = v[:, -1] * F
    v = np.argmax(v, axis=1)

    mask = v <= np.max(x[:, -1])
    fine_grid = fine_grid[mask]

    print("Filtered grid: {}".format(fine_grid.shape))

    dist = np.zeros((len(files), len(files)))
    for i, f in enumerate(files):
        p, _ = ref_prob(f, fine_grid, 3, 50000)
        kls = calculate_kl(p, files, fine_grid, 3, 50000)
        dist[i, :] = kls

    if overwrite:
        filename = "{}/Lipids/dscribe_{}{}/distance_full_{}_ang".format(HOME, system, TR, cutoff)
        np.save(filename, dist)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("-s", dest="system", type=str,
                        help="4beads or phospate file")

    parser.add_argument("-c", dest="cutoff", type=int,
                        help="config file")

    parser.add_argument("-z", dest="sample", type=int,
                        help="sample size")

    parser.add_argument("-ow", dest="overwrite", type=str2bool, default=True,
                        help="overwrite")

    args = parser.parse_args()

    main(args.system, args.cutoff, args.sample, bool(args.overwrite))
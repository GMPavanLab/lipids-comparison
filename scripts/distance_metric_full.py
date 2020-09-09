import glob
import time
import argparse

import numpy as np

from tools import *


def main(system, cutoff, sample, overwrite=True):

    prefix = "{}/Lipids/dscribe_{}{}/pca/{}_ang/".format(HOME, system, TR, cutoff)
    files = sorted(glob.glob("{}POPC_*npy".format(prefix)))

    files = [i for i in files if '303' in i]
    print('Processing {} trajectories at 303k'.format(len(files)))

    grid_filename = "{}/Lipids/dscribe_{}{}/grid_{}_ang.npy".format(HOME, system, TR, cutoff)
    fine_grid = np.load(grid_filename)

    print("Filtered grid: {}".format(fine_grid.shape))

    ref_probs = []
    for i, f in enumerate(files):
        x = np.load(f)
        tmp = average_predict(x, fine_grid, PCA_DIMENSIONS, sample, D_thr, 10)
        f_suffix = f.split('/')[-1][:-4]
        p_filaname = "{}/Lipids/dscribe_{}{}/probs/probs_{}_ang_{}.npy".format(HOME, system, TR, cutoff, f_suffix)
        np.save(p_filaname, tmp)
        ref_probs.append(tmp)

    dist = np.zeros((len(files), len(files)))
    for i, f in enumerate(files):
        for j, f in enumerate(files):
            if i >= j:
                dist[i, j] = JS(ref_probs[i], ref_probs[j])

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

    parser.add_argument("-ow", dest="overwrite", type=str2bool, default=False,
                        help="overwrite")

    args = parser.parse_args()

    main(args.system, args.cutoff, args.sample, bool(args.overwrite))
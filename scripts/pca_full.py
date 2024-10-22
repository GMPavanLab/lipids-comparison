import glob
import time
import argparse
import pathlib

import numpy as np
from dscribe.descriptors import SOAP
from sklearn.decomposition import PCA
import joblib

from tools import *


def main(system, cutoff, sample, overwrite=True):

    prefix = (
        "{}/data/dscribe_{}{}/full_soap/{}_ang/".format(HOME, system, TR, cutoff)
    )

    X = []

    for full_atom in FULL_ATOM:

        x = np.load(prefix + full_atom)['arr_0']   
        indices = np.arange(x.shape[0])
        np.random.shuffle(indices)
        X.append(x[indices[:sample]])

    X = np.vstack(X)

    pca = PCA(n_components=10)
    pca.fit(X)

    folder = (
        "{}/data/dscribe_{}{}/pca/{}_ang/".format(HOME, system, TR, cutoff)
    )

    pathlib.Path(folder).mkdir(parents=True, exist_ok=True)

    joblib.dump(pca, folder + 'pca.pkl')

    files = sorted(glob.glob("{}POPC_*npz".format(prefix)))
    print('Processing trajectories at 303k')
    files = [i for i in files if '303' in i]

    if overwrite:

        for f in files:
            print("extrapolating on {}".format(f))
            save_name = folder + f[:-4].split('/')[-1]
            x = np.load(f)['arr_0']   
            out = pca.transform(x)
            np.save(save_name, out)


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
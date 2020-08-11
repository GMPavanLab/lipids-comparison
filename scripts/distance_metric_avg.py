import glob
import time
import argparse

import numpy as np
from dscribe.descriptors import SOAP

from shared import *


def main(system, cutoff, average, overwrite=True):

    files = sorted(glob.glob('{}/Lipids/dscribe_{}{}/avg_soap/{}_ang/POPC_*npz'.format(HOME, system, TR, cutoff)))
    print('Processing only 303k for now')
    files = [i for i in files if '303' in i]

    dist = np.zeros((len(files), len(files)))

    for i, f1 in enumerate(files):

        x1 = np.load(f1)['arr_0']   
        soap1 = x1.mean(axis=0)

        for j, f2 in enumerate(files):
	    
            if f1 != f2:

                print(i, j)
                x2 = np.load(f2)['arr_0']   
                soap2 = x2.mean(axis=0)

                dist[i, j] = DistanceSoap(soap1, soap2)

    if overwrite:
        filename = "{}/Lipids/dscribe_{}{}/distance_avg_{}_ang".format(HOME, system, TR, cutoff)
        np.save(filename, dist)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("-s", dest="system", type=str,
                        help="4beads or phospate file")

    parser.add_argument("-c", dest="cutoff", type=int,
                        help="config file")

    parser.add_argument("-ow", dest="overwrite", type=str2bool, default=False,
                        help="overwrite")

    args = parser.parse_args()

    main(args.system, args.cutoff, bool(args.overwrite))
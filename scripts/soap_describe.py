import glob
import time
import argparse

import numpy as np
from dscribe.descriptors import SOAP

from shared import *


species = {
    "4beads": ["N", "P", "C"],
    "phosphate": ["P"]
}

def get_folder(average):
    return "avg_soap" if average == "inner" else "full_soap"


def main(system, cutoff, average, overwrite=True):

    files = sorted(glob.glob('{}/Lipids/trajectories_{}{}/POPC_*xyz'.format(HOME, system, TR)))
    print('Processing trajectories at 303k')
    files = [i for i in files if '303' in i]
    folder = '{}/Lipids/dscribe_{}{}/{}/{}_ang/'.format(HOME, system, TR, get_folder(average), cutoff)

    if not os.path.isdir(folder):
        os.mkdir(folder)

    for f in files:
	    
        save_name = folder + f[:-4].split('/')[-1]
        
        if not os.path.isfile(save_name + '.npz') or overwrite: 

            soap_input = dict(
                average=average,
                periodic=True,
                species=species[system],
                rcut=cutoff,
                nmax=8,
                lmax=8,
            )

            traj = read_traj(f)
            SIZE = min(len(traj), MAX_TRAJ_SIZE)

            box = np.loadtxt(f[:-4] + '.box')[-MAX_TRAJ_SIZE:,:]
            traj = traj[-MAX_TRAJ_SIZE:]
            
            for i, j in enumerate(traj):
                traj[i].set_cell(list(box[i]))
                traj[i].set_pbc([1, 1, 0])

            tt = time.time()

            soap = SOAP(**soap_input)

            N = len(traj)
            pos = [list(np.where(traj[0].get_atomic_numbers() == 15)[0])]
            soap_vec = soap.create(traj, positions=pos * N)

            np.savez_compressed(save_name, soap_vec)
            print('saved {}'.format(save_name), time.time() - tt)
	    
        else:
	        print('skip {}'.format(save_name))

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("-s", dest="system", type=str,
                        help="4beads or phospate file")

    parser.add_argument("-c", dest="cutoff", type=int,
                        help="config file")

    parser.add_argument("-a", dest="average", type=str, default="off",
                        help="perform average")

    parser.add_argument("-ow", dest="overwrite", type=str2bool, default=False,
                        help="overwrite")

    args = parser.parse_args()

    main(args.system, args.cutoff, args.average, bool(args.overwrite))
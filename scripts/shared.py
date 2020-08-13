import os

import numpy as np
from ase.io import read
from Pipeline.DPA import DensityPeakAdvanced
from sklearn.neighbors import NearestNeighbors, KNeighborsClassifier
from scipy.stats import entropy


HOME = os.path.expanduser("~")

TR = "_1us"

MAX_TRAJ_SIZE = 4000

def grouper(iterable, n):
    if len(iterable) % 3 != 0:
        raise ValueError(f"Iterable's length is not a multiple of {n}")
    return zip(*(iter(iterable),) * n)


def frame2string(coord):
    write = ""
    for i, frame in enumerate(coord):
        write += "%d\nAutoGen_%d\n" % (len(coord[0]), i)
        for mol in frame:
            write += "       N{:12.5f}{:11.5f}{:11.5f}\n".format(*mol)
    return write


def read_traj(filename, index=":", start=None, end=None, stride=None):
    if all([start, end, stride]):
        index = "{}:{}:{}".format(start, end, stride),
    return read(filename, index=index, format="xyz")


def KernelSoap(x, y, n):
    return ( np.dot(x, y) / (np.dot(x, x) * np.dot(y, y)) ** 0.5 ) ** n


def DistanceSoap(x, y, n=1):
    try:
        return (2.0 - 2.0 * KernelSoap(x, y, n)) ** 0.5
    except FloatingPointError:
        return 0


def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise ValueError('Boolean value expected.')


def cartesian_product(arrays):
    la = len(arrays)
    dtype = np.result_type(*arrays)
    arr = np.empty([la] + [len(a) for a in arrays], dtype=dtype)
    for i, a in enumerate(np.ix_(*arrays)):
        arr[i, ...] = a
    return arr.reshape(la, -1).T


class UniformGrid:
    
    def __init__(self, mode='minmax', percentile=5):
        self.mode = mode
        self.percentile = percentile
        self.dim = None
        self.minmax = {}
        
    def get_ranges(self, x):
        if self.mode == 'minmax':
            l, u = x.min(), x.max()
        elif self.mode == 'precentile':
            l, u = np.percentile(x, self.percentile), np.percentile(x, 100 - self.percentile)
        else:
            raise ValueError('Mode not available')
            
        return l, u
        
            
    def fit(self, x):
        self.dim = x.shape[1]
        for dim in range(self.dim):
            self.minmax[dim] = self.get_ranges(x[:, dim])
        return self
    
    def transform(self, n):
        ranges = []
        for dim in range(self.dim):
            spacing = ( self.minmax[dim][1] - self.minmax[dim][0] ) / n
            ranges.append(
                np.linspace(
                    self.minmax[dim][0] - spacing / 2, 
                    self.minmax[dim][1] + spacing / 2, 
                    n
                )
            )
        return cartesian_product(ranges)
    

def filter_grid(grid, sample_points, neigh=10):
    knn = KNeighborsClassifier(neigh)
    x = np.vstack([grid, sample_points])
    x, y = x[:,:-1], x[:, -1:]
    knn.fit(x, y.reshape((x.shape[0],)).astype(int))
    return knn


def extract_sample(files, sample_size=5000):
    X = []
    for i, file in enumerate(files):
        x = np.load(file)
        np.random.shuffle(x)
        x = x[:sample_size,:]
        x = np.hstack([x, np.zeros([x.shape[0], 1]) + i])
        X.append(x)
    return np.vstack(X)


def KL(p, q):
    return np.sum(p * np.log(p / q))


def JS(p, q):
    m = (p + q) / 2
    return (entropy(p, m)[0] + entropy(q, m)[0]) / 2


def predict(d, k, x):
    densities = np.exp(np.array(d.densities_))
    values = []
    for row in x:
        dist, indices = k.kneighbors(row.reshape(1, -1))
        v = np.dot(1 / dist, densities[indices][0]) / np.sum(1 / dist)
        values.append(v)
    return np.log(values)


def ref_prob(filename, grid, n, size, D_thr=15):
    x = np.load(filename)[:size, :n]
    nn = NearestNeighbors(n_neighbors=3).fit(x)
    dens = DensityPeakAdvanced(D_thr=D_thr, k_max=500).fit(x)
    return predict(dens, nn, grid), x


def calculate_js(p, files, fine_grid, n, size):
    kls = []
    for file in files:
        x = np.load(file)
        np.random.shuffle(x)
        x = x[:size, :n]
        print(x.shape)
        nn = NearestNeighbors(n_neighbors=3).fit(x)
        dens = DensityPeakAdvanced(k_max=500).fit(x)
        q = predict(dens, nn, fine_grid)
        kl = JS(p, q)
        kls.append(kl)
        print(file, kl)
        
    return kls
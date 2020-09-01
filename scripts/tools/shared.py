import numpy as np
from Pipeline.DPA import DensityPeakAdvanced
from sklearn.neighbors import NearestNeighbors, KNeighborsClassifier

from .utils import cartesian_product, lazy_cartesian_product
from .metrics import JS


class UniformGrid:
    """
    This class is used to generate an uniform grid based on the range of values
    contained in a reference dataset.
    """
    def __init__(self, mode='minmax', percentile=5):
        self.mode = mode
        self.percentile = percentile
        self.dim = None
        self.minmax = {}
        
    def get_ranges(self, x):
        if self.mode == 'minmax':
            l, u = x.min(), x.max()
        elif self.mode == 'percentile':
            l, u = np.percentile(x, self.percentile), np.percentile(x, 100 - self.percentile)
        else:
            raise ValueError('Mode not available')
            
        return l, u
        
    def fit(self, x):
        """
        Determination of ranges of value for grid creation.
        """
        self.dim = x.shape[1]
        for dim in range(self.dim):
            self.minmax[dim] = self.get_ranges(x[:, dim])
        return self
    
    def _transform(self, n):
        """
        Returns list of ranges for grid creation.
        """
        ranges = []
        for dim in range(self.dim):
            spacing = ( self.minmax[dim][1] - self.minmax[dim][0] ) / n
            ranges.append(
                list(
                    np.linspace(
                        self.minmax[dim][0] - spacing / 2, 
                        self.minmax[dim][1] + spacing / 2, 
                        n
                    )
                )
            )
        return ranges

    def transform(self, n):
        """
        Create grid as a generator in chunk is size `chunk` for lazy evaluation.
        """
        return cartesian_product(self._transform(n))


    def lazy_transform(self, n, chunk=100):
        """
        Create grid as a generator in chunk is size `chunk` for lazy evaluation.
        """
        return lazy_cartesian_product(self._transform(n), chunk)
    

def fit_grid_refiner(grid, sample_points, neigh=10):
    """
    Fit a KNeighborsClassifier to filter out gridpoints which
    are not likely to be meaninful.
    """
    knn = KNeighborsClassifier(neigh)
    x = np.vstack([grid, sample_points])
    x, y = x[:,:-1], x[:, -1:]
    knn.fit(x, y.reshape((x.shape[0],)).astype(int))
    return knn


def filter_grid(knn, fine_grid_iter, f):
    """
    Filter grid created by grid generator using classifier and
    output the result.
    """
    filtered = []
    for it in fine_grid_iter:
        if it.shape[0]: 
            v = knn.predict_proba(it)
            v[:,-1] = v[:, -1] * f
            v = np.argmax(v, axis=1)

            mask = v <= it.shape[1] 
            filtered.append(it[mask])
    return np.vstack(filtered)


def extract_sample(files, sample_size=5000):
    """
    Extract a sample of size `sample_size` from each dataset in files.
    """
    X = []
    for i, file in enumerate(files):
        x = np.load(file)
        np.random.shuffle(x)
        x = x[:sample_size,:]
        x = np.hstack([x, np.zeros([x.shape[0], 1]) + i])
        X.append(x)
    return np.vstack(X)


def average_predict(x, grid, D, size, D_thr, folds):
    """
    Average the probability density estimates on the fine grid by reapeating the 
    fitting on subsample of the original dataset.
    """
    preds = []
    for i in range(folds):
        np.random.shuffle(x)
        X = x[:size, :D]
        print('Average predict: size {}, fold {}'.format(X.shape[0], i))
        nn = NearestNeighbors(n_neighbors=3).fit(X)
        print('\tFitted nearest neighbors')
        dens = DensityPeakAdvanced(D_thr=D_thr, k_max=500).fit(X)
        print('\tFitted density peak')
        tmp = predict(dens, nn, grid).reshape(-1, 1)
        print('\tPredicted')
        preds.append(tmp)
    return np.hstack(preds).mean(0)


def predict(d, k, x):
    """
    Use NearestNeighbors to interpolate densities on out of sample values.
    """
    densities = np.exp(np.array(d.densities_))
    values = []
    for row in x:
        dist, indices = k.kneighbors(row.reshape(1, -1))
        v = np.dot(1 / dist, densities[indices][0]) / np.sum(1 / dist)
        values.append(v)
    return np.log(values)


def ref_prob(filename, grid, n, size, D_thr=15):
    """
    Calculculate reference probabilities.
    """
    x = np.load(filename)[:size, :n]
    nn = NearestNeighbors(n_neighbors=3).fit(x)
    dens = DensityPeakAdvanced(D_thr=D_thr, k_max=500).fit(x)
    return predict(dens, nn, grid), x


def calculate_js(p, files, fine_grid, n, size):
    """
    Jensen–Shannon divergence for reference densities p with all dataset in
    files on grid.
    """
    kls = []
    for file in files:
        x = np.load(file)
        np.random.shuffle(x)
        x = x[:size, :n]
        print(x.shape)
        nn = NearestNeighbors(n_neighbors=3).fit(x)
        dens = DensityPeakAdvanced(k_max=500).fit(x)
        q = predict(dens, nn, fine_grid)
        kl = JS(p, q)[0]
        kls.append(kl)
    return kls
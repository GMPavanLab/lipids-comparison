import itertools
import ase.io
import numpy as np


def cartesian_product(ranges):
    """
    Explicit grid genereation.
    """
    ranges = [np.array(i) for i in ranges]
    la = len(ranges)
    dtype = np.result_type(*ranges)
    arr = np.empty([la] + [len(a) for a in ranges], dtype=dtype)
    for i, a in enumerate(np.ix_(*ranges)):
        arr[i, ...] = a
    return arr.reshape(la, -1).T


def _lazy_cartesian_product(ranges):
    """
    Generate grid using iteratools.product.
    """
    return itertools.product(*ranges)


def lazy_cartesian_product(arrays, size=100):
    """
    Group generator in array of size `size`.
    """
    x = []
    for i,v in enumerate(_lazy_cartesian_product(arrays)):
        if not (i + 1) % size:
            x.append(v)
            yield np.array(x)
            x = []
        else:
            x.append(v)
    yield np.array(x)


def str2bool(v):
    """
    Convert string to boolean for argument parsing. 
    """
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise ValueError('Boolean value expected.')


def grouper(iterable, n):
    """
    Group iterable exaclty by n.
    """
    if len(iterable) % n != 0:
        raise ValueError(f"Iterable's length is not a multiple of {n}")
    return zip(*(iter(iterable),) * n)


def frame2string(coord):
    """
    Convert a xyz frame to string.
    """
    write = ""
    for i, frame in enumerate(coord):
        write += "%d\nAutoGen_%d\n" % (len(coord[0]), i)
        for mol in frame:
            write += "       N{:12.5f}{:11.5f}{:11.5f}\n".format(*mol)
    return write


def read_traj(filename, index=":", start=None, end=None, stride=None):
    """
    Read xyz trajectory into a ase.Atoms object.
    """
    if all([start, end, stride]):
        index = "{}:{}:{}".format(start, end, stride),
    return ase.io.read(filename, index=index, format="xyz")

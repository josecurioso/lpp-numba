import numpy as np
import numba as nb


@nb.jit(nopython=True, parallel=True, fastmath=True)
def kernel(M, float_n, data):

    # mean = np.mean(data, axis=0)
    mean = np.sum(data, axis=0) / float_n
    # stddev = np.std(data, axis=0)
    stddev = np.sqrt(np.sum((data - mean)**2, axis=0) / float_n)
    stddev[stddev <= 0.1] = 1.0
    data = np.subtract(data, mean)
    data = np.divide(data, np.sqrt(float_n) * stddev)
    corr = np.eye(M, dtype=data.dtype)
    for i in nb.prange(M - 1):
        corr[i + 1:M, i] = corr[i, i + 1:M] = data[:, i] @ data[:, i + 1:M]

    return corr

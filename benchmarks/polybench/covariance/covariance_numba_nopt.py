import numpy as np
import numba as nb


@nb.jit(nopython=True, parallel=True, fastmath=True)
def kernel(M, float_n, data):

    #mean = np.mean(data, axis=0)
    mean = np.sum(data, axis=0) / float_n
    data = np.subtract(data, mean)
    cov = np.zeros((M, M), dtype=data.dtype)
    for i in range(M):
        cov[i:M, i] = cov[i, i:M] = data[:, i] @ data[:, i:M] / (float_n - 1.0)

    return cov

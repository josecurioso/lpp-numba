import numpy as np
import numba as nb


@nb.jit(nopython=True, parallel=True, fastmath=True)
def kernel(path):

    for k in range(path.shape[0]):
        # path[:] = np.minimum(path[:], np.add.outer(path[:, k], path[k, :]))
        for i in nb.prange(path.shape[0]):
            path[i, :] = np.minimum(path[i, :], path[i, k] + path[k, :])

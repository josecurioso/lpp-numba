import numpy as np
import numba as nb


@nb.jit(nopython=True, parallel=True, fastmath=True)
def kernel(alpha, beta, C, A, B):

    C[:] = alpha * A @ B + beta * C

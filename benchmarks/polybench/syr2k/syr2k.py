# Copyright 2021 ETH Zurich and the NPBench authors. All rights reserved.

import numpy as np


def initialize(M, N, datatype=np.float64):
    alpha = datatype(1.5)
    beta = datatype(1.2)
    C = np.fromfunction(lambda i, j: ((i * j + 3) % N) / M, (N, N),
                        dtype=datatype)
    A = np.fromfunction(lambda i, j: ((i * j + 1) % N) / N, (N, M),
                        dtype=datatype)
    B = np.fromfunction(lambda i, j: ((i * j + 2) % M) / M, (N, M),
                        dtype=datatype)

    return alpha, beta, C, A, B

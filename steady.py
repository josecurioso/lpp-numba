#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import sys
import bench

if __name__ == "__main__":

    if len(sys.argv) < 7:
        print("""Pass me:
        1) the command to execute
        2) the confidence level (between 0 and 1)
        3) p (number of iterations)
        4) the percentage that, when reached, the loop breaks
        5) max benchmark invocations
        6) k (the number of last measurements to be considered)
        7) CoV (coefficient of variation)""")
    else:
        command = sys.argv[1]
        confidence_level = float(sys.argv[2])
        p_iterations = int(sys.argv[3])
        break_if_error_percentage_is = float(sys.argv[4])
        max_bench_iterations = int(sys.argv[5])
        k = int(sys.argv[6])
        CoV = float(sys.argv[7])
        interval, mean, sdev, error_percentage = bench.steady(command, confidence_level, p_iterations, break_if_error_percentage_is, max_bench_iterations, k, CoV)
        print("Results Steady State:")
        print("Interval:", interval)
        print("Mean:", mean)
        print("Standard deviation:", sdev)
        print("Interval percentage:", error_percentage)



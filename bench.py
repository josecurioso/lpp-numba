#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import scipy
import numpy
import scipy.stats.distributions as distributions
import math
import os
import time
from subprocess import PIPE, Popen
from process_timer import ProcessTimer

platform = "python"

def confidence(samples, confidence_level):
    """This function determines the confidence interval for a given set of samples,
    as well as the mean, the standard deviation, and the size of the confidence
    interval as a percentage of the mean.
    """
    mean = numpy.mean(samples)
    sdev = numpy.std(samples)
    n = len(samples)
    df = n - 1
    t = distributions.t.ppf((1+confidence_level)/2.0, df)
    interval = (interval_low, interval_high) = mean - t * sdev / math.sqrt(n) , mean + t * sdev / math.sqrt(n)
    interval_size = interval_high - interval_low
    error_percentage = interval_size / mean * 100.0
    values = [value for value in samples if value >= interval_low and value <= interval_high] if len(samples) > 1 else samples
    
    print(values)
    return interval, numpy.mean(values), numpy.std(values), error_percentage

def startup(command, data, confidence_level, p_iterations, break_if_error_percentage_is):
    f = open("current.py", "w")
    f.write(command)
    f.close()
    execution_times = []
    for i in range(1, p_iterations+1):
        #before = time.time()
        #os.system("python current.py")
        #after = time.time()

        process = Popen(args=platform+" current.py", stdout=PIPE, shell=True)
        process_std_output = process.communicate()[0]
        execution_time = float(process_std_output.splitlines()[-1])

        print("Iteration %s. Times in millis %s." % (i, execution_time))
        execution_times.append(execution_time)
    interval, mean, sdev, error_percentage = confidence(execution_times, confidence_level)
    return interval, mean, sdev, error_percentage

def memory(command, data, confidence_level, p_iterations, break_if_error_percentage_is):
    f = open("current.py", "w")
    f.write(command)
    f.close()
    memory_measures = []
    for i in range(1, p_iterations+1):
        ptimer = ProcessTimer([platform,'current.py'])

        try:
            ptimer.execute()
            #poll as often as possible; otherwise the subprocess might 
            # "sneak" in some extra memory usage while you aren't looking
            while ptimer.poll():
                time.sleep(.1)
        finally:
            #make sure that we don't leave the process dangling?
            ptimer.close()

        print("Iteration %s. Max memory %s." % (i, ptimer.max_rss_memory))
        memory_measures.append(ptimer.max_rss_memory)
    interval, mean, sdev, error_percentage = confidence(memory_measures, confidence_level)
    return interval, mean, sdev, error_percentage

def steady(command, data, confidence_level, p_iterations, break_if_error_percentage_is, max_bench_invocations, k, CoV):
    command = command.format(m_b_i=max_bench_invocations, _k=k, c_o_v=CoV)
    f = open("current.py", "w")
    f.write(command)
    f.close()

    execution_times = []
    for i in range(1, p_iterations+1):
        process = Popen(args=platform+" current.py", stdout=PIPE, shell=True)
        process_std_output = process.communicate()[0]
        execution_time = float(process_std_output.splitlines()[-1])


        #loc = {}
        #exec(command, {**(globals()), **data}, loc)
        #execution_time = loc['return_time']
        print("Iteration %s. Times in millis %s." % (i, execution_time))
        execution_times.append(execution_time)
        interval, mean, sdev, error_percentage = confidence(execution_times, confidence_level)
        if error_percentage <= break_if_error_percentage_is:
            break
    return interval, mean, sdev, error_percentage

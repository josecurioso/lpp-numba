#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import
from benchmark import Benchmark
import bench
import pathlib
import os
import pickle

resultsFile = open("results_.csv", "a")
resultsFile.write("mode;bench;version;int_min;int_max;mean;std;error\n")

def show(interval, mean, sdev, error_percentage):
    print("\tInterval: {}.".format(interval))
    print("\tMean: {}.".format(mean))
    print("\tStandard deviation: {}.".format(sdev))
    print("\tError percentage: {:.2f}%.".format(error_percentage))


def prepare_benchmark(benchmark: Benchmark, version: str):
    data = benchmark.get_data()
    module_pypath = "benchmarks.{r}.{m}".format(
            r=benchmark.info["relative_path"].replace('/', '.'),
            m=benchmark.info["module_name"])
    module_str = "{m}_{p}".format(m=module_pypath, p=version)
    func_str = benchmark.info["func_name"]

    
    del data['__builtins__']
    data_assign = ""
    base = "{key}={_data}"
    for k in data.keys():
        data_assign+=base.format(key=k, _data=data[k])+"\n"

    output = open("data.pickle", "wb")
    pickle.dump(data, output)



    template = """from {m} import {f} as impl
import pickle
import time

inputfile = open("data.pickle", "rb")
data = pickle.load(inputfile)
locals().update(data)

before = time.time()
impl({args})
after = time.time()
print((after-before)*1000)
    """
    

    templateSteady = """
import pickle
import time
import numpy
import math

inputfile = open("data.pickle", "rb")
data = pickle.load(inputfile)
locals().update(data)

def runSteady():
    max_bench_invocations={{m_b_i}}
    k={{_k}}
    CoV={{c_o_v}}
    
    def getMean(execs, k):
        return numpy.mean(execs[-k:])
        
    def areWeDone(execs, k, CoV):
        if(len(execs)<k):
            return False
        suma = 0
        mean = getMean(execs, k)
        last = execs[-k:]
        for t in last:
            suma = suma + pow(t-mean, 2)
        std = math.sqrt(suma/k)

        return (std/mean) < CoV
        
    execution_times = []
    c = 0
    from {m} import {f} as impl
    while (c<max_bench_invocations):
        before = time.time()
        impl({args})
        after = time.time()
        execution_time = (after-before)*1000
        execution_times.append(execution_time)
        if(areWeDone(execution_times, k, CoV)):
            print(execution_times)
            return getMean(execution_times, k)
        c+=1
    return getMean(execution_times, k)

print(runSteady())
    """
    return {'c': template.format(m=module_str, f=func_str, args=', '.join(benchmark.info["input_args"])),#, data=data_assign),
            'cSteady': templateSteady.format(m=module_str, f=func_str, args=', '.join(benchmark.info["input_args"])),
            'd': data}

def run_benchmark(benchname: str, version: str):
    ready = prepare_benchmark(Benchmark(benchname), version)
    
    try:
        print("------{b} STARTUP: {v}------".format(b=benchname, v=version))
        interval, mean, sdev, error_percentage = bench.startup(ready['c'], ready['d'], 0.95, 30, 0)
        print("Results Startup:")
        show(interval, mean, sdev, error_percentage)
        resultsFile.writelines(["{mode};{bench};{version};{int_min};{int_max};{mean};{std};{error}\n".format(mode="startup", bench=benchname, version=version, int_min=interval[0], int_max=interval[1], mean=mean, std=sdev, error=error_percentage)])
    except Exception as e:
        print(e)
        resultsFile.writelines(["{mode};{bench};{version}\n".format(mode="startup", bench=benchname, version=version)])
    
    
    try:
        print("------{b} STEADY-STATE: {v}------".format(b=benchname, v=version))
        interval, mean, sdev, error_percentage = bench.steady(ready['cSteady'], ready['d'], 0.95, 30, 0, 15, 5, 0.02)
        print("Results Steady-state:")
        show(interval, mean, sdev, error_percentage)
        resultsFile.writelines(["{mode};{bench};{version};{int_min};{int_max};{mean};{std};{error}\n".format(mode="steady", bench=benchname, version=version, int_min=interval[0], int_max=interval[1], mean=mean, std=sdev, error=error_percentage)])
    except Exception as e:
        print(e)
        resultsFile.writelines(["{mode};{bench};{version}\n".format(mode="steady", bench=benchname, version=version)])
    
    try:
        print("------{b} MEMORY: {v}------".format(b=benchname, v=version))
        interval, mean, sdev, error_percentage = bench.memory(ready['c'], ready['d'], 0.95, 30, 0)
        print("Results Memory:")
        show(interval, mean, sdev, error_percentage)
        resultsFile.writelines(["{mode};{bench};{version};{int_min};{int_max};{mean};{std};{error}\n".format(mode="memory", bench=benchname, version=version, int_min=interval[0], int_max=interval[1], mean=mean, std=sdev, error=error_percentage)])
    except Exception as e:
        print(e)
        resultsFile.writelines(["{mode};{bench};{version}\n".format(mode="memory", bench=benchname, version=version)])

if __name__ == "__main__":    
    parent_folder = pathlib.Path(__file__).parent.absolute()
    bench_dir = parent_folder.joinpath("bench_info")
    pathlist = pathlib.Path(bench_dir).rglob('*.json')
    benchnames = [os.path.basename(path)[:-5] for path in pathlist]
    benchnames.sort()
    
    benchnames.remove('conv2d_bias')

    def runBench(name):
        run_benchmark(name, "numpy_copt")
        run_benchmark(name, "numba_nopt")

    
    for benchname in benchnames:
        runBench(benchname)
    
    """
    run_benchmark("conv2d_bias", "numba_copt")
    run_benchmark("conv2d_bias", "numba_nopt")
    run_benchmark("conv2d_bias", "numpy_copt")
    run_benchmark("conv2d_bias", "numpy_nopt")
    """
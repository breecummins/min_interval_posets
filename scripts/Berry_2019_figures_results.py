from min_interval_posets.curve import Curve
from min_interval_posets import posets
import os
import pandas
from copy import deepcopy


def extractdata(filename):
    file_type = filename.split(".")[-1]
    if file_type == "tsv":
        df = pandas.read_csv(open(filename),delim_whitespace=True)
    elif file_type == "csv":
        df = pandas.read_csv(open(filename))
    else:
        raise ValueError("File type not recognized. Require .tsv or .csv.")
    return list(df)[1:],df.values


def row(filename):
    times,data = extractdata(filename)
    times = [float(n) for n in times]
    names = data[:,0]
    curves = [Curve(data[k,1:],times,True) for k in range(data.shape[0])]
    # plt.plot(times,data[0,1:],marker="o")
    # plt.show()
    return dict(zip(names,curves))


def col(filename):
    names,data = extractdata(filename)
    times = data[:,0]
    curves = [Curve(data[1:,k],times,True) for k in range(data.shape[1])]
    return dict(zip(names,curves))


def getposets(filename,filestyle,epsilons,names="all",start_time=None,end_time=None):
    '''

    :param filename: Name of the time series data file. Include absolute or relative path to file.
    :param filestyle: "row" if the time points lie in a single row, or "col" if they lie in a column
    :param epsilons: list of floats between 0 and 1
    :param names: list of gene names on which to create poset. If "all" (default), then all genes in the file are used
    :return: list of partial orders, one for each epsilon
    '''
    if filestyle == "row":
        curves = row(os.path.expanduser(filename))
    elif filestyle == "col":
        curves = col(os.path.expanduser(filename))
    else:
        raise ValueError("Filestyle not recognized.")
    subset_curves = deepcopy(curves)
    names = names if names is not "all" else []
    for name in curves:
        if name not in names:
            subset_curves.pop(name)
    if start_time is not None and end_time is not None:
        subset_curves = {name : Curve(curve.trim(start_time,end_time)) for name,curve in subset_curves.items()}
    return posets.eps_posets(subset_curves, epsilons)

from min_interval_posets.curve import Curve
from min_interval_posets import posets
from min_interval_posets import triplet_merge_trees as tmt
from min_interval_posets import sublevel_sets as ss
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


def getcurves(filename,filestyle,names,start_time,end_time):
    '''

    :param filename: Name of the time series data file. Include absolute or relative path to file.
    :param filestyle: "row" if the time points lie in a single row, or "col" if they lie in a column
    :param names: list of gene names on which to create curve. If "all" (default), then all genes in the file are used
    :param start_time: front trim for time series in time units
    :param end_time: back trim for time series in time units
    :return: list of curve objects
    '''
    if filestyle == "row":
        curves = row(os.path.expanduser(filename))
    elif filestyle == "col":
        curves = col(os.path.expanduser(filename))
    else:
        raise ValueError("Filestyle not recognized.")
    subset_curves = deepcopy(curves)
    for name in curves:
        if names != "all" and name not in names:
            subset_curves.pop(name)
    if start_time is not None and end_time is not None:
        subset_curves = {name : Curve(curve.trim(start_time,end_time)) for name,curve in subset_curves.items()}
    return subset_curves


def getposets(filename,filestyle,epsilons,names="all",start_time=None,end_time=None):
    '''

    :param filename: Name of the time series data file. Include absolute or relative path to file.
    :param filestyle: "row" if the time points lie in a single row, or "col" if they lie in a column
    :param epsilons: list of floats between 0 and 1
    :param names: list of gene names on which to create poset. If "all" (default), then all genes in the file are used
    :param start_time: front trim for time series in time units
    :param end_time: back trim for time series in time units
    :return: list of partial orders, one for each epsilon
    '''
    subset_curves = getcurves(filename,filestyle,names,start_time,end_time)
    return posets.eps_posets(subset_curves, epsilons)


def getintervals(filename,filestyle,epsilons,names,start_time,end_time):
    '''

    :param filename: Name of the time series data file. Include absolute or relative path to file.
    :param filestyle: "row" if the time points lie in a single row, or "col" if they lie in a column
    :param epsilons: list of floats between 0 and 1
    :param names: list of gene names on which to create intervals. If "all" (default), then all genes in the file are used
    :param start_time: front trim for time series in time units
    :param end_time: back trim for time series in time units
    :return: dict of tuples of (eps, intervals), one item for each name in names
    '''

    subset_curves = getcurves(filename,filestyle,names,start_time,end_time)
    intervals = dict()
    for name,curve in subset_curves.items():
        intervals[name] = []
        for eps in epsilons:
            n = curve.normalize()
            r = curve.normalize_reflect()
            merge_tree_mins = tmt.births_only(n)
            merge_tree_maxs = tmt.births_only(r)
            time_ints_mins = ss.get_sublevel_sets(merge_tree_mins, n, eps)
            time_ints_maxs = ss.get_sublevel_sets(merge_tree_maxs, r, eps)
            labeled_mins = sorted([(v, (name, "min")) for _, v in time_ints_mins.items()])
            labeled_maxs = sorted([(v, (name, "max")) for _, v in time_ints_maxs.items()])
            # When eps is close to (b-a)/2 for max b and min a, then the intervals can be identical. Annihilate them.
            nodes = posets.annihilate(sorted(labeled_mins + labeled_maxs))
            intervals[name].append((eps,nodes))
    return intervals


























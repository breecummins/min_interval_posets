from libposets.curve import Curve
import libposets.posets as posets
import os
import pandas
import matplotlib.pyplot as plt
import numpy as np

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
    A = np.asarray([v for (i,v) in curves[0].curve.items()])
    plt.plot(times, A)
    # plt.plot(times, -1*A,marker="o")
    plt.show()
    return dict(zip(names,curves))

def col(filename):
    names,data = extractdata(filename)
    times = data[:,0]
    curves = [Curve(data[1:,k],times,True) for k in range(data.shape[1])]
    return dict(zip(names,curves))

def getposets(filename,filestyle,epsilons):
    '''

    :param filename: Name of the time series data file. Include absolute or relative path to file.
    :param filestyle: "row" if the time points lie in a single row, or "col" if they lie in a column
    :param epsilons: list of floats between 0 and 1
    :return: list of partial orders, one for each epsilon
    '''
    if filestyle == "row":
        curves = row(os.path.expanduser(filename))
    elif filestyle == "col":
        curves = col(os.path.expanduser(filename))
    else:
        raise ValueError("Filestyle not recognized.")
    return posets.eps_posets(curves,epsilons)

def troubleshoot(filename):
    import libposets.triplet_merge_trees as tmt
    import libposets.sublevel_sets as ss
    eps = 0.005
    c = row(os.path.expanduser(filename))["A"].normalize_reflect()
    merge_tree_maxs = tmt.births_only(c)
    print(merge_tree_maxs)
    sublvl = ss.get_sublevel_sets(merge_tree_maxs,c,eps)
    print(sublvl)
    times = sorted([k for k in c])
    b = 104
    i = times.index(b)
    k = i
    print("forward")
    while k < len(times)-1 and abs(c[times[k]] - c[times[i]]) < 2*eps:
        print(times[k])
        print(c[times[k]])
        k += 1
        print(k)
    j = i
    print("backward")
    while j > 0 and abs(c[times[j]] - c[times[i]]) < 2*eps:
        print(times[j])
        print(c[times[j]])
        j -= 1
        print(j)
    print((times[j+1],times[k-1]))

def test():
    x = np.arange(-np.pi,np.pi,0.01)
    curve = {"A" : Curve(np.cos(x),x)}
    print(posets.eps_posets(curve, [0.02]))

def test2():
    eps = 0.1
    c = row(os.path.expanduser(filename))["A"]
    print(posets.eps_posets({"A":c}, [eps]))



if __name__ == "__main__":
    filename = "~/Simulations/Pipeline/20180904/clipped_LEMmanu_Fig3B-network_synnet_10-5-1_c2spc25.tsv"
    filestyle = "row"
    epsilons = [0.05]
    # posets = getposets(filename,filestyle,epsilons)
    # print(posets)
    # troubleshoot(filename)
    test2()

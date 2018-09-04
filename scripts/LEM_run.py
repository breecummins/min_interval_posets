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
    plt.plot(times, -1*A)
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
    print(curves)
    return posets.eps_posets(curves,epsilons)

if __name__ == "__main__":
    filename = "~/Simulations/Pipeline/20180904/clipped_LEMmanu_Fig3B-network_synnet_10-5-1_c2spc25.tsv"
    filestyle = "row"
    epsilons = [0.1]
    posets = getposets(filename,filestyle,epsilons)
    print(posets)

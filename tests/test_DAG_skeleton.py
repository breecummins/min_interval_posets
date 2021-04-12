from min_interval_posets.curve import Curve
from min_interval_posets import DAG_skeleton as ds
import numpy as np

def test1():
    c1 = Curve({0:1, 5:10, 10:3})
    c2 = Curve({0:8, 5:3, 10:1})
    nodesA = ds.get_nodes('A', c1.curve)
    nodesB = ds.get_nodes('B', c2.curve)
    assert(nodesA == [(0, ('A', 'min')), (5, ('A', 'max')), (10, ('A', 'min'))])
    assert(nodesB == [(0, ('B', 'max')), (10, ('B', 'min'))])
    curves = {'A':c1, 'B':c2}
    DAGskeleton = ds.get_DAGskeleton(curves)
    assert(DAGskeleton == ([(0, ('A', 'min')), (5, ('A', 'max')), (10, ('A', 'min')), (0, ('B', 'max')),(10, ('B', 'min'))],
                           [(0, 1), (0, 2), (0, 4), (1, 2), (1, 4), (3, 1), (3, 2), (3, 4)]))

def test2():
    x = np.arange(0,2*np.pi,0.1)   # start,stop,step
    y = np.sin(x)
    z = np.cos(x)
    c1 = Curve({x[i]:y[i] for i in range(len(x))})
    c2 = Curve({x[i]:z[i] for i in range(len(y))})
    sinnodes = ds.get_nodes('sine', c1.curve)
    cosnodes = ds.get_nodes('cosine', c2.curve)
    assert(sinnodes == [(0.0, ('sine', 'min')), (1.6, ('sine', 'max')), (4.7, ('sine', 'min')),(6.2, ('sine', 'max'))])
    assert(cosnodes == [(0.0, ('cosine', 'max')), (3.1, ('cosine', 'min')), (6.2, ('cosine', 'max'))])
    curves = {'sine':c1, 'cosine':c2}
    DAGskeleton = ds.get_DAGskeleton(curves)
    assert(DAGskeleton == ([(0.0, ('sine', 'min')), (1.6, ('sine', 'max')), (4.7, ('sine', 'min')), (6.2, ('sine', 'max')),
                          (0.0, ('cosine', 'max')), (3.1, ('cosine', 'min')), (6.2, ('cosine', 'max'))],
                          [(0, 1), (0, 2), (0, 3), (0, 5), (0, 6), (1, 2), (1, 3), (1, 5), (1, 6), (2, 3), (2, 6), (4, 1),
                          (4, 2), (4, 3), (4, 5), (4, 6), (5, 2), (5, 3), (5, 6)]))

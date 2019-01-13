from min_interval_posets.curve import Curve
from min_interval_posets.triplet_merge_trees import *

def test():

    # integer curve 1
    curve = Curve({0:-2, 1:2, 2:0, 3:3, 4:-4, 5:1, 6:-7})
    tmt = {0:(3,6),1:(1,0),2:(1,0),3:(3,6),4:(5,6),5:(5,6),6:(6,6)}
    assert(tmt == compute_merge_tree(curve.curve))
    assert(tmt == compute_merge_tree(curve.normalize()))
    tMt = {0:(0,3),1:(2,3),2:(2,3),3:(3,3),4:(4,3),5:(4,3),6:(6,3)}
    assert(tMt == compute_merge_tree(curve.reflect()))
    assert(tMt == compute_merge_tree(curve.normalize_reflect()))

    # integer curve 2
    curve2 = Curve({0:0, 1:-1, 2:-2, 3:1, 4:3, 5:6, 6:2})
    tmt2 = {0:(0,2),1:(1,2),2:(2,2),3:(3,2),4:(4,2),5:(5,2),6:(5,2)}
    assert(tmt2 == compute_merge_tree(curve2.curve))
    assert(tmt2 == compute_merge_tree(curve2.normalize()))
    tMt2 = {0:(2,5),1:(1,0),2:(2,5),3:(3,5),4:(4,5),5:(5,5),6:(6,5)}
    assert(tMt2 == compute_merge_tree(curve2.reflect()))
    assert(tMt2 == compute_merge_tree(curve2.normalize_reflect()))

    import numpy as np
    # discretized smooth curve
    # round entries to avoid round-off errors
    x = np.arange(-2.5, 5.01, 0.01)
    y = -0.25 * x ** 4 + 4.0/3 * x ** 3 + 0.5 * x ** 2 - 4.0 * x
    curve = Curve({round(t,2): round(v,10) for (t, v) in zip(x, y)})
    tmt = {-2.5: (-2.5, -2.5), 5.0: (4.0, -2.5), 1.0: (-1.0, -2.5)}
    assert(tmt == births_only(curve.curve))

    # discretized symmetric smooth curve
    # round entries to avoid round-off errors
    # identical depth minima are labeled by first occurrence
    x = np.arange(-0.75,0.76,0.01)
    y = 0.25*x**2*(x**2 - 0.5)
    curve = Curve({round(t,2): round(v,10) for (t, v) in zip(x, y)})
    tmt = {-0.5 : (-0.5,-0.5), 0.5 : (0.0,-0.5)}
    assert(tmt == births_only(curve.curve))
    tMt = {-0.75 : (-0.75,-0.75), 0.0 : (-0.5,-0.75), 0.75 : (0.5,-0.75)}
    print(births_only(curve.reflect()))
    assert (tMt == births_only(curve.reflect()))


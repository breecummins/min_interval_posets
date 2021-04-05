from min_interval_posets.curve import Curve
from min_interval_posets import eps_intersection as ei
import numpy as np

def test1():
    c1 = Curve({0:1, 5:10, 10:3})
    c2 = Curve({0:8, 5:3, 10:1})
    epssup1 = ei.get_eps_sup(0, c1, 4.5)
    assert(epssup1 == (0,5))
    epssup2 = ei.get_eps_sup(0, c1, 4.6)
    assert(epssup2 == (0,10))
    checkintersection = ei.intervals_intersect(0, 10, c1, c2, 1)
    assert(checkintersection == True)
    epsjumps1 = ei.get_eps_jumps(0, c1.curve)
    assert(epsjumps1 == [0, 4.5])
    epsjumps2 = ei.get_eps_jumps(0, c2.curve)
    assert(epsjumps2 == [0, 2.5, 3.5])
    epsintersection = ei.get_eps_intersection(0, 10, c1, c2)
    assert(epsintersection == 0)

def test2():
    x = np.arange(0,2*np.pi,0.1)   # start,stop,step
    y = np.sin(x)
    z = np.cos(x)
    c1 = Curve({x[i]:y[i] for i in range(len(x))})
    c2 = Curve({x[i]:z[i] for i in range(len(y))})
    curves = {"sine":c1, "cosine":c2}
    epsintersection1 = ei.get_eps_intersection(1.6, 6.2, c1, c2)
    epsintersection2 = ei.get_eps_intersection(0, 6.2, c1, c2)
    assert(epsintersection1 == 0.8250928589434148)
    assert(epsintersection2 == 0.49978680152075255)

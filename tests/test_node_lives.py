from min_interval_posets.curve import Curve
from min_interval_posets.node_lives import get_node_lives
import numpy as np

def test1():
    c1 = Curve({0:1, 5:10, 10:3})
    nodelives = get_node_lives(c1)
    assert(nodelives == {0: 4.5, 10: 3.5, 5: 4.5})
    
def test2():
    c2 = Curve({0:8, 5:3, 10:1})
    nodelives = get_node_lives(c2)
    assert(nodelives == {10: 3.5, 0: 3.5})

def test3():
    c3 = Curve({0:0, 1:2, 4:5, 5:1, 7:10, 10:7})
    nodelives = get_node_lives(c3)
    assert(nodelives == {0: 5.0, 5: 2.0, 10: 1.5, 4: 2.0, 7: 5.0})

def test4():
    x = np.arange(0,2*np.pi,0.1)   # start,stop,step
    y = np.sin(x)
    c4 = Curve({x[i]:y[i] for i in range(len(x))})
    nodelives = get_node_lives(c4)
    nodelives_round = {u:round(nodelives[u], 8) for u in nodelives.keys()}
    assert(nodelives_round == {0.0: 0.4997868, 4.7: 0.99974843, 1.6: 0.99974843, 6.2: 0.45841693})

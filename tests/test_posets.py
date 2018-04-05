from libposets.curve import Curve
from libposets.posets import *
import numpy as np

def test():
    '''
    Note: Assertions may fail due to noise level. Check if zero noise level is returning correctly.
    If so, reduce the random noise levels and see if that fixes the problem.
    '''

    x = np.arange(-2.5,5.01,0.01)
    y = -0.25*x**4 + 4.0/3*x**3 + 0.5*x**2 - 4.0*x
    z = 0.6 * (0.25 * x ** 4 - 1.6 / 3 * x ** 3 - 4.35 / 2 * x ** 2 + 0.45 * x)
    noises = [0.0, 0.001, 0.002] #have to have very small noise for posets to stay the same.

    def check_output_singles(u,pos,noise_std,eps):
        np.random.seed(0)
        noise = np.random.normal(0,noise_std,u.shape)
        curve = Curve({ round(t,2) : round(v,10) for (t,v) in zip(x,u+noise) })
        assert(pos == get_poset(get_mins_maxes("curve",curve,eps)))

    def check_output_doubles(pos,n,eps):
        print(eps)
        np.random.seed(0)
        noise = np.random.normal(0,n,y.shape)
        curvey = Curve({ round(t,2) : round(v,10) for (t,v) in zip(x,y+noise) })
        curvez = Curve({ round(t,2) : round(v,10) for (t,v) in zip(x,z+noise) })
        print(main({"y":curvey,"z":curvez},[eps])[0])
        assert(pos == main({"y":curvey,"z":curvez},[eps])[0])

    epsilons = [0.01,0.05]
    posy1 = ((('curve', 'min'), ('curve', 'max'), ('curve', 'min'), ('curve', 'max'), ('curve', 'min')),
           [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)])
    posz1 = ((('curve', 'max'), ('curve', 'min'), ('curve', 'max'), ('curve', 'min'), ('curve', 'max')),
           [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)])
    posb1 = ((('y', 'min'), ('y', 'max'), ('y', 'min'), ('y', 'max'), ('y', 'min'), ('z', 'max'), ('z', 'min'), ('z', 'max'), ('z', 'min'), ('z', 'max')), [(0, 1), (0, 2), (0, 3), (0, 4), (0, 6), (0, 7), (0, 8), (0, 9), (1, 2), (1, 3), (1, 4), (1, 8), (1, 9), (2, 3), (2, 4), (2, 8), (2, 9), (3, 4), (3, 9), (5, 1), (5, 2), (5, 3), (5, 4), (5, 6), (5, 7), (5, 8), (5, 9), (6, 2), (6, 3), (6, 4), (6, 7), (6, 8), (6, 9), (7, 3), (7, 4), (7, 8), (7, 9), (8, 3), (8, 4), (8, 9)])
    posy5 = ((('curve', 'min'), ('curve', 'max'), ('curve', 'min')), [(0, 1), (0, 2), (1, 2)])
    posz5 = ((('curve', 'min'), ('curve', 'max')), [(0, 1)])
    posb5 = ((('y', 'min'), ('y', 'max'), ('y', 'min'), ('z', 'min'), ('z', 'max')), [(0, 1), (0, 2), (0, 4), (1, 2), (1, 4), (3, 2), (3, 4)])
    posets = ((posy1,posz1,posb1),(posy5,posz5,posb5))
    for (eps,pos) in zip(epsilons,posets):
        for n in noises:
            check_output_singles(y,pos[0],n,eps)
            check_output_singles(z,pos[1],n,eps)
            check_output_doubles((eps,pos[2]), n, eps)
    eps = 0.0025
    pos=((('y', 'min'), ('y', 'max'), ('y', 'min'), ('y', 'max'), ('y', 'min'), ('z', 'max'), ('z', 'min'), ('z', 'max'), ('z', 'min'), ('z', 'max')), [(0, 1), (0, 2), (0, 3), (0, 4), (0, 6), (0, 7), (0, 8), (0, 9), (1, 2), (1, 3), (1, 4), (1, 7), (1, 8), (1, 9), (2, 3), (2, 4), (2, 8), (2, 9), (3, 4), (3, 9), (5, 1), (5, 2), (5, 3), (5, 4), (5, 6), (5, 7), (5, 8), (5, 9), (6, 1), (6, 2), (6, 3), (6, 4), (6, 7), (6, 8), (6, 9), (7, 2), (7, 3), (7, 4), (7, 8), (7, 9), (8, 3), (8, 4), (8, 9)])
    check_output_doubles((eps,pos), 0, eps)


import numpy as np

class Curve(object):

    def __init__(self,curve,perturb=1.e-10):
        '''
        Collection of methods on dictionary representation of function.
        :param curve: a dictionary representing a function, float times keying float values
        :param perturb: small perturbation float
       '''
        if any((not isinstance(x, (int, float))) or (not isinstance(y, (int, float))) for x,y in curve.items()):
            raise ValueError("Curve must be of type {number : number}.")
        self.curve = curve

    def normalize(self):
        '''
        Normalize function in [-0.5,0.5].
        :return: a dictionary representing a normalized function, times key values
        '''
        times = [t for t in self.curve]
        vals = np.array([self.curve[t] for t in times])
        nvals = (vals - float(np.min(vals))) / (np.max(vals) - np.min(vals)) - 0.5
        return dict((t, n) for (t, n) in zip(times, nvals))

    def reflect(self):
        '''
        Reflect curve over the x-axis.
        :return: a dictionary representing a function, times key sign-reversed values
        '''
        return dict((t,-1*n) for (t,n) in self.curve.items())

    def normalize_reflect(self):
        '''
        Normalize function in [-0.5,0.5] and reflect over the x-axis.
        :return: a dictionary representing a normalized function, times key sign-reversed values
        '''
        N = self.normalize()
        return dict((t,-1*n) for (t,n) in N.items())

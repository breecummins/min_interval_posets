import numpy as np

class Curve(object):

    def __init__(self,curve,times=None,norm=False):
        '''
        Collection of methods on dictionary representation of function.
        :param curve: a dictionary representing a function, float times keying float values
        OR
        :param curve: length N list or numpy array of numerical values
        :param times: length N list or numpy array of time points (numbers)
       '''
        if times is None:
            if any((not isinstance(x, (int, float))) or (not isinstance(y, (int, float))) for x,y in curve.items()):
                raise ValueError("Curve must be of type {number : number}.")
            self.curve = curve
        else:
            if not isinstance(times[0],(int,float)) or not isinstance(curve[0],(int,float)):
                raise ValueError("Parameters 'curve' and 'times' must be arrays of numbers.")
            else:
                self.curve = dict(zip(times,curve))
        if norm:
            self.curve = self.normalize()

    def normalize(self):
        '''
        Normalize function in [-0.5,0.5].
        :return: a dictionary representing a normalized function, times key values
        '''
        times = [t for t in self.curve]
        vals = np.array([self.curve[t] for t in times])
        # nvals = (vals - float(np.min(vals))) / (np.max(vals) - np.min(vals)) - 0.5
        if np.max(vals) - np.min(vals):
            nvals = (vals - float(np.min(vals))) / (np.max(vals) - np.min(vals)) - 0.5
        else:
            nvals = np.asarray([0]*len(times))
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

    def trim(self,start_time,end_time):
        '''
        Trim function according to start and end times.

        :param start_time: Float or int representing earliest desired time.
        :param end_time: Float or int representing last desired time.
        :return: a dictionary representing a trimmed function, times key values
        '''
        times = sorted([t for t in self.curve])
        vals = np.array([self.curve[t] for t in times])
        start_ind = next(iter([x[0] for x in enumerate(times) if x[1] >= start_time]),0)
        end_ind = next(iter([x[0] for x in enumerate(times) if x[1] > end_time]),len(times))
        return dict((t, n) for (t, n) in zip(times[start_ind:end_ind], vals[start_ind:end_ind]))

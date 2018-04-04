import sys
sys.path.append('../libposets')
import libposets.triplet_merge_trees as tmt
import libposets.sublevel_sets as ss

def get_mins_maxes(name,curve,eps):
    '''
    For a given (named) curve and threshold eps, find the eps-minimum intervals of
    both the maxima and minima of the curve.
    :param name: A string uniquely identifying the time series (curve).
    :param curve: dict with float times keying float function values
    :param eps: float threshold (noise level) with 0 < eps < 1.
    :return: sorted list of tuples where first element is sublevel set interval and
             second element is name + extrema type
    '''
    n = curve.normalize()
    r = curve.normalize_reflect()
    merge_tree_mins = tmt.births_only(n)
    merge_tree_maxs = tmt.births_only(r)
    time_ints_mins = ss.minimal_time_ints(merge_tree_mins,n,eps)
    time_ints_maxs = ss.minimal_time_ints(merge_tree_maxs,r,eps)
    labeled_mins = [(v,(name,"min")) for _,v in time_ints_mins.items()]
    labeled_maxs = [(v,(name,"max")) for _,v in time_ints_maxs.items()]
    both = sorted(labeled_mins+labeled_maxs)
    both = prune_overlap(both[:])
    extrema = [b[1][-3:] for b in both]
    if any(x==y for (x,y) in zip(extrema[:-1],extrema[1:])):
        # This shouldn't ever happen
        raise ValueError("Two minima or two maxima in a row.")
    return both

def prune_overlap(both):
    # get rid of overlapping mins and maxs

    def combine(sublist):
        m = sorted([o[0][0] for o in sublist])[0]
        M = sorted([o[0][1] for o in sublist])[-1]
        both.append(((m, M), sublist[0][1]))

    z = list(zip(both[:-1],both[1:]))
    overlap = set([])
    while len(z) > 0:
        (a,b) = z.pop(0)
        while a[0][1] > b[0][0]:
            overlap.add(a)
            overlap.add(b)
            (a,b) = z.pop(0)
        if len(overlap)%2 == 1:
            mins = [o for o in overlap if o[1][1]=="min"]
            if len(mins) > len(overlap)/2.0:
                combine(mins)
            else:
                maxs = [o for o in overlap if o[1][1]=="max"]
                combine(maxs)
        for o in overlap:
            both.remove(o)
        overlap = set([])
    both.sort()
    return both

def get_poset(all_extrema):
    ints,names = zip(*all_extrema)
    edges = []
    for j,a in enumerate(ints):
        for k,b in enumerate(ints):
            # <= means interpret tuples as open intervals
            # <  means interpret tuples as closed intervals
             if a[1] <= b[0]:
                edges.append((j,k))
    return names,edges


def main(curves,epsilons):
    '''
    Construct posets on multiple curves over multiple epsilons.
    :param curves: dict of instances of Curve, each keyed by unique name
    :param epsilons: list of threshold epsilons
    :return: list of posets, one for each epsilon, unless epsilon gets too large to distinguish extrema
    '''
    posets = []
    for eps in sorted(epsilons):
        all_extrema = []
        for name,curve in curves.items():
            ae = get_mins_maxes(name,curve,eps)
            if len(ae) > 1:
                all_extrema.extend(ae)
            else:
                print("Warning: Epsilon = {:.3f} is too large to distinguish extrema. No poset returned.".format(eps))
                return posets
        posets.append(get_poset(all_extrema))
    return posets

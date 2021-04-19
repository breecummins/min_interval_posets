def get_sublevel_sets(births_only_merge_tree,curve,eps,eps_restriction=True):
    '''
    Calculates the sublevel set interval for every minimum in curve that exceeds a threshold.
    :param births_only_merge_tree: merge tree dict with intermediate points removed
    :param curve: dict with times keying function values (Curve.curve or Curve.normalized)
    :param eps: float threshold (noise level) For normalized curves, 0 < eps < 1.
    :return: dict of minima birth times keying lifetime intervals
    '''
    if eps_restriction:
        big_enough = [u for u,(s,v) in births_only_merge_tree.items() if not(u!=v and abs(curve[u] - curve[s]) < 2*eps)]
    else:
        big_enough = [u for u,_ in births_only_merge_tree.items()]
    times = sorted([k for k in curve])
    time_intervals = dict()
    for b in big_enough:
        i = times.index(b)
        k = i
        # the reason why we need 2*eps instead of eps is in the paper Berry et al.
        while k < len(times)-1 and (curve[times[k]] < curve[times[i]] or (curve[times[k]] >= curve[times[i]] and abs(curve[times[k]] - curve[times[i]]) < 2*eps)):
            k += 1
        j = i
        # the reason why we need 2*eps instead of eps is in the paper Berry et al.
        while j > 0 and (curve[times[j]] < curve[times[i]] or (curve[times[j]] >= curve[times[i]] and abs(curve[times[j]] - curve[times[i]]) < 2*eps)):
            j -= 1
        time_intervals[b] = (times[j],times[k])
    return time_intervals


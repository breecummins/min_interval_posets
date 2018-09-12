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
    labeled_mins = sorted([(v,(name," min"),T) for T,v in time_ints_mins.items()])
    labeled_maxs = sorted([(v,(name," max"),T) for T,v in time_ints_maxs.items()])
    nodes = sorted(labeled_mins+labeled_maxs)
    # when a max and min are very close together on a flattish extremum, then the extremum
    # can have both a max and a min label. The following code picks one.
    prev=0
    new_nodes = []
    for m,p in zip(nodes[:-1],nodes[1:]):
        if m == prev:
            continue
        elif m[0][0] == p[0][0]:
            new_nodes.append((m,p))
            prev = p
        else:
            new_nodes.append(m)
    if prev != nodes[-1]:
        new_nodes+=[nodes[-1]]
    # must handle case where all nodes are paired
    # NOTE: len(g)==2 is fragile!! If the length of a labeled extremum changes from 3 to 2, this breaks!!
    if all([len(g)==2 for g in new_nodes]):
        #FIXME: The algorithm in this if clause does not correctly handle single points
        raise RuntimeError("This case is not implemented.")
        n0 = new_nodes[0][0]
        label = n0[1][1].strip()
        for t in n:
            tot = 0
            num = 0
            if t >= n0[0][0] and t <= n0[0][1]:
                tot += n[t]
                num += 1
        if (n0[2] > tot/num and label == "max") or (n0[2] < tot/num and label == "min"):
            new_nodes[0] = n0
        else:
            new_nodes[0] = new_nodes[0][1]
    # now get rid of duplicate labels
    while any([len(m)==2 for m in new_nodes]):
        for k,g in enumerate(new_nodes):
            if len(g)==2:
                if k > 0 and not(len(new_nodes[k-1])==2):
                    if "max" in new_nodes[k-1][1][1]:
                        new_nodes[k] = g[0] if "min" in g[0][1][1] else g[1]
                        continue
                    if "min" in new_nodes[k-1][1][1]:
                        new_nodes[k] = g[0] if "max" in g[0][1][1] else g[1]
                        continue
                if k < len(new_nodes)-1 and not(len(new_nodes[k-1])==2):
                    if "max" in new_nodes[k+1][1][1]:
                        new_nodes[k] = g[0] if "min" in g[0][1][1] else g[1]
                        continue
                    if "min" in new_nodes[k+1][1][1]:
                        new_nodes[k] = g[0] if "max" in g[0][1][1] else g[1]
                        continue
    nodes = [N[:-1] for N in new_nodes]
    # print(nodes)
    # print("\n")
    # check that extrema do oscillate
    extrema = [n[1][-3:] for n in nodes]
    if any(x==y for (x,y) in zip(extrema[:-1],extrema[1:])):
        # This shouldn't ever happen
        print(nodes)
        raise ValueError("Two minima or two maxima in a row.")
    elif len(extrema)==1:
        # get rid of constant functions
        nodes = []
    # make within time series edges; [a,b] < [c,d] only if a < c
    edges = [(i,j) for i, n in enumerate(nodes) for j, m in enumerate(nodes) if n[0][0] < m[0][0]]
    return nodes, edges


def get_poset(nodes,edges):
    '''
    Construct transitive closure of partial order.

    :param nodes: all extrema from all time series along with their epsilon-extremal intervals
    :param edges: within time series edges, which are calculated differently than between time series edges
    :return: labels of nodes and edges between nodes based on the index of the label
    '''
    edges = set(edges)
    ints,names = zip(*nodes)
    for j,a in enumerate(ints):
        for k,b in enumerate(ints):
            # interpret tuples as closed intervals, i.e. [a,b] < [c,d] only if b < c
            if a[1] < b[0]:
                edges.add((j, k))
    return names,edges


def eps_posets(curves,epsilons):
    '''
    Construct posets on multiple curves over multiple epsilons.
    :param curves: dict of instances of Curve, each keyed by unique name
    :param epsilons: list of threshold epsilons
    :return: list of posets, one for each epsilon
    '''
    posets = []
    for eps in sorted(epsilons):
        all_nodes = []
        all_edges = []
        for name,curve in curves.items():
            nodes, edges = get_mins_maxes(name,curve,eps)
            N = len(all_nodes)
            all_nodes.extend(nodes)
            all_edges.extend([(i+N,j+N) for (i,j) in edges])
        posets.append((eps,get_poset(all_nodes,all_edges)))
    return posets

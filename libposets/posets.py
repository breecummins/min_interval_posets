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
    labeled_mins = sorted([(v,(name," min")) for _,v in time_ints_mins.items()])
    labeled_maxs = sorted([(v,(name," max")) for _,v in time_ints_maxs.items()])
    nodes = sorted(labeled_mins+labeled_maxs)
    # when a max and min are very close together on a flattish extremum, then the extremum
    # can have both a max and a min label. The following code picks one.
    prev=0
    grpnodes = []
    for m,n in zip(nodes[:-1],nodes[1:]):
        if m == prev:
            prev = n
            continue
        elif m[0][0] == n[0][0]:
            grpnodes.append((m,n))
            prev = n
        else:
            grpnodes.append(m)
            prev = n
    new_nodes = grpnodes[:]
    # must handle case where all nodes are paired
    if all([type(g) is tuple for g in grpnodes]):
        n0 = grpnodes[0][0]
        n1 = grpnodes[1][0]
        for
        if sum(n0[0])
        t = n0[1]
        label = n0[1][1][1:]
        if label == "min" and n[]
    while 0 in new_nodes:
        for k,g in enumerate(grpnodes):
            if type(g) is tuple:
                if k > 0 and not(type(new_nodes[k-1]) is tuple):
                    if "max" in new_nodes[k-1][1][1]:
                        new_nodes[k] = g[0] if "min" in g[0][1][1] else g[1]
                        continue
                    if "min" in new_nodes[k-1][1][1]:
                        new_nodes[k] = g[0] if "max" in g[0][1][1] else g[1]
                        continue
                elif k < len(grpnodes)-1 and not(type(new_nodes[k+1]) is tuple):
                    if "max" in new_nodes[k+1][1][1]:
                        new_nodes[k] = g[0] if "min" in g[0][1][1] else g[1]
                        continue
                    if "min" in new_nodes[k+1][1][1]:
                        new_nodes[k] = g[0] if "max" in g[0][1][1] else g[1]
                        continue



    print(nodes)
    extrema = [n[1][-3:] for n in nodes]
    if any(x==y for (x,y) in zip(extrema[:-1],extrema[1:])):
        # This shouldn't ever happen
        print(nodes)
        raise ValueError("Two minima or two maxima in a row.")
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

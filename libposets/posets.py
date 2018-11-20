import sys
sys.path.append('../libposets')
import libposets.triplet_merge_trees as tmt
import libposets.sublevel_sets as ss


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
            nodes, edges = get_total_order(name,curve,eps)
            N = len(all_nodes)
            all_nodes.extend(nodes)
            all_edges.extend([(i+N,j+N) for (i,j) in edges])
        posets.append((eps,get_poset(all_nodes,all_edges)))
    return posets


def get_total_order(name,curve,eps):
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
    # time_ints_mins = ss.minimal_time_ints(merge_tree_mins,n,eps)
    # time_ints_maxs = ss.minimal_time_ints(merge_tree_maxs,r,eps)
    time_ints_mins = ss.get_sublevel_sets(merge_tree_mins,n,eps)
    time_ints_maxs = ss.get_sublevel_sets(merge_tree_maxs,r,eps)
    labeled_mins = sorted([(v,(name,"min")) for _,v in time_ints_mins.items()])
    labeled_maxs = sorted([(v,(name,"max")) for _,v in time_ints_maxs.items()])
    # When eps is close to (b-a)/2 for max b and min a, then the intervals can be identical. Annihilate them.
    nodes = annihilate(sorted(labeled_mins+labeled_maxs))
    # check that extrema do oscillate
    extrema = [n[1] for n in nodes]
    if any(x==y for (x,y) in zip(extrema[:-1],extrema[1:])):
        # Should never get two minima or two maxima in a row. If there are, a bug fix is required.
        raise ValueError("Two minima or two maxima in a row: {}.".format(nodes))
    # make within time series edges; [a,b] < [c,d] only if a < c
    edges = [(i,j) for i, n in enumerate(nodes) for j, m in enumerate(nodes) if n[0][0] < m[0][0] or n[0][1] < m[0][1]]
    return nodes, edges


def annihilate(nodes):
    # Get rid of intervals that are dual labeled
    prev=None
    new_nodes = []
    for m,p in zip(nodes[:-1],nodes[1:]):
        if m[0] == p[0]:
            new_nodes.append((m,p))
            prev = p
        elif m!= prev:
            new_nodes.append((m,))
    if prev != nodes[-1]:
        new_nodes+=[(nodes[-1],)]
    if any([len(g)==2 for g in new_nodes]):
        print("Annhilation occured.")
    return [m[0] for m in new_nodes if len(m)==1]


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
            # interpret tuples as open intervals, i.e. (a,b) < (c,d) only if b <= c
            if a[1] <= b[0]:
                edges.add((j, k))
    return names,edges


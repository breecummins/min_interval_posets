import sys
sys.path.append('../libposets')
import libposets.triplet_merge_trees as tmt
import libposets.sublevel_sets as ss
from warnings import warn


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
    # when a max and min are very close together on a flattish extremum, then the extremum
    # can have both a max and a min label. The following function resolves this.
    nodes = handle_dual_labeled_intervals(sorted(labeled_mins+labeled_maxs),name,eps)
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


def handle_dual_labeled_intervals(nodes,name,eps):
    # This ugly function handles the sticky case where there are both maxima and minima on a flattish extremum.
    # First identify intervals where this occurs and collect the paired labels.
    prev=None
    new_nodes = []
    for m,p in zip(nodes[:-1],nodes[1:]):
        if m[0][0] == p[0][0]:
            new_nodes.append((m,p))
            prev = p
        elif m!= prev:
            new_nodes.append((m,))
    if prev != nodes[-1]:
        new_nodes+=[(nodes[-1],)]
    # now choose one of min/max on same interval using information from singletons
    # must first handle case where all nodes ended up paired
    if all([len(g)==2 for g in new_nodes]):
        warn("There are two possibilities for the linear order of {} at epsilon = {}. \nOne is chosen at random. To resolve, try increasing epsilon.".format(name,eps))
        new_nodes[0] = (new_nodes[0][0],)
    # maxes and mins must alternate, so propagate the information given by singletons
    while any([len(m)==2 for m in new_nodes]):
        for k,g in enumerate(new_nodes):
            if len(g)==2:
                if k > 0 and len(new_nodes[k-1])==1:
                    new_nodes[k] = (g[0],) if g[0][1][1] != new_nodes[k-1][0][1][1] else (g[1],)
                elif k < len(new_nodes)-1 and len(new_nodes[k+1])==1:
                    new_nodes[k] = (g[0],) if g[0][1][1] != new_nodes[k+1][0][1][1] else (g[1],)
    nodes = [N[0] for N in new_nodes]
    # check that extrema do oscillate
    extrema = [n[1][-3:] for n in nodes]
    if any(x==y for (x,y) in zip(extrema[:-1],extrema[1:])):
        # Should never get two minima or two maxima in a row. If there are, a bug fix is required.
        raise ValueError("Two minima or two maxima in a row: {}.".format(nodes))
    elif len(extrema)==1:
        # get rid of constant functions
        warn("Time series {} is constant at epsilon = {} and is not included in the partial order. \nTo resolve, try decreasing epsilon.".format(name,eps))
        nodes = []
    return nodes



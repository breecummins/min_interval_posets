def compute_merge_tree(curve):
    '''
    :param curve: dict with float times keying function float values (Curve.curve)
    :return: triplet merge tree representation --
             a dict with a time keying a tuple of times, T[u] = (s,v),
             where u obtains label v at time s (branch decomposition)

    reference: Dmitriy Smirnov and Dmitriy Morozov Chapter 1 Triplet Merge Trees
    people.csail.mit.edu/smirnov/publications/tmt.pdf
    Algorithms 1 & 2
    To appear in Topological Methods in Data Analysis and Visualization V
    (Proceedings of TopoInVis 2017).
    '''

    def finddeepest(u):
        u1 = deepest[u]
        (_,v) = T[u1]
        while u1 != v:
            u1 = deepest[v]
            (_,v) = T[u1]
        d = u1
        u1 = deepest[u]
        (_, v) = T[u1]
        while u1 != v:
            u1 = deepest[v]
            deepest[v] = d
            (_, v) = T[u1]
        deepest[u] = d
        return d

    T = dict( (t,(t,t)) for t in curve )
    deepest = dict( (t,t) for t in curve )
    times = sorted([t for t in curve])
    edges = list(zip(times[:-1],times[1:]))
    sorted_verts = [a for (a,b) in sorted(curve.items(), key=lambda t : (t[1],t[0]))]
    for u in sorted_verts:
        leaves = []
        for e in edges:
            if u in e:
                v = e[0] if u != e[0] else e[1]
                if curve[v] < curve[u]:
                    leaves.append(finddeepest(v))
        if len(leaves) > 0:
            inds = sorted(zip([sorted_verts.index(l) for l in leaves],leaves))
            w = min(inds)[1]
            T[u] = (u,w)
            leaves.remove(w)
            for x in leaves:
                T[x] = (u,w)
    return T


def births_only(curve):
    '''
    Computes merge tree and then removes all intermediate points and keeps only minima.
    :param curve: dict with times keying function values (Curve.curve or Curve.normalized)
    :return: triplet merge tree representation --
             a dict with a time keying a tuple of times, T[u] = (s,v),
             where u obtains label v at time s (branch decomposition)
    '''
    merge_tree = compute_merge_tree(curve)
    no_births = [u for u, (s, v) in merge_tree.items() if u == s and u!=v]
    for u in no_births:
        merge_tree.pop(u)
    return merge_tree










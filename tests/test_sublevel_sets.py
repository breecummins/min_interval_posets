import libposets.triplet_merge_trees as tmt
from libposets.curve import Curve
from libposets.sublevel_sets import *


def test():
    # integer curve 1
    curve = Curve({0:-2, 1:2, 2:0, 3:3, 4:-4, 5:1, 6:-7})
    births_only_merge_tree = tmt.births_only(curve.curve)
    eps = 0.75
    ti = get_sublevel_sets(births_only_merge_tree,curve.curve,eps)
    assert(ti == {0: (0, 0), 2: (2, 2), 4: (4, 4), 6: (6, 6)})
    time_ints = minimal_time_ints(births_only_merge_tree, curve.curve, eps)
    assert(time_ints=={0: (0, 0), 2: (2, 2), 4: (4, 4), 6: (6, 6)})
    eps=2
    ti = get_sublevel_sets(births_only_merge_tree,curve.curve,eps)
    assert(ti == {0: (0, 2), 4: (4, 4), 6: (6, 6)})
    time_ints = minimal_time_ints(births_only_merge_tree, curve.curve, eps)
    assert(time_ints=={0: (0, 2), 4: (4, 4), 6: (6, 6)})
    eps=3
    ti = get_sublevel_sets(births_only_merge_tree,curve.curve,eps)
    assert(ti == {6: (6, 6)})
    time_ints = minimal_time_ints(births_only_merge_tree, curve.curve, eps)
    assert(time_ints=={6: (6, 6)})

    # integer curve 2
    curve2 = Curve({0:0, 1:-1, 2:-2, 3:1, 4:3, 5:6, 6:2})
    births_only_merge_tree = tmt.births_only(curve2.curve)
    time_ints = minimal_time_ints(births_only_merge_tree, curve2.curve, 0.75)
    assert(time_ints == {2: (1, 2), 6: (6, 6)})
    time_ints = minimal_time_ints(births_only_merge_tree, curve2.curve, 1)
    assert(time_ints == {2: (0, 2), 6: (6, 6)})
    eps=3
    ti = get_sublevel_sets(births_only_merge_tree,curve2.curve,eps)
    assert(ti == {2: (0, 4)})
    time_ints = minimal_time_ints(births_only_merge_tree, curve2.curve, eps)
    assert(time_ints == {2: (0, 4)})

from min_interval_posets import triplet_merge_trees as tmt
from min_interval_posets.curve import Curve
from min_interval_posets.sublevel_sets import *


def test():
    # integer curve 1
    curve = Curve({0:-2, 1:2, 2:0, 3:3, 4:-4, 5:1, 6:-7})
    births_only_merge_tree = tmt.births_only(curve.curve)
    ti = get_sublevel_sets(births_only_merge_tree,curve.curve,0.75)
    assert(ti == {0: (0, 1), 2: (1, 3), 4: (3, 5), 6: (5, 6)})
    ti = get_sublevel_sets(births_only_merge_tree,curve.curve,2)
    assert(ti == {0: (0, 1), 4: (3, 5), 6: (5, 6)})
    ti = get_sublevel_sets(births_only_merge_tree,curve.curve,3)
    assert(ti == {6: (5, 6)})

    # integer curve 2
    curve2 = Curve({0:0, 1:-1, 2:-2, 3:1, 4:3, 5:6, 6:2})
    births_only_merge_tree = tmt.births_only(curve2.curve)
    time_ints = get_sublevel_sets(births_only_merge_tree, curve2.curve, 0.75)
    assert(time_ints == {2: (0, 3), 6: (5, 6)})
    time_ints = get_sublevel_sets(births_only_merge_tree, curve2.curve, 1)
    assert(time_ints == {2: (0, 3), 6: (5, 6)})
    ti = get_sublevel_sets(births_only_merge_tree,curve2.curve,3)
    assert(ti == {2: (0, 5)})

    # curve 3 with 3 equal points
    curve3 = Curve({0:2,1:0,2:0,3:0,4:2,5:3,6:3,7:3,8:1.5,9:0})
    births_only_merge_tree = tmt.births_only(curve3.curve)
    time_ints = get_sublevel_sets(births_only_merge_tree, curve3.curve,0.5)
    assert(time_ints == {1: (0, 4), 9: (8, 9)})
    time_ints = get_sublevel_sets(births_only_merge_tree, curve3.curve,1.1)
    assert(time_ints == {1: (0, 5), 9: (7, 9)})
    time_ints = get_sublevel_sets(births_only_merge_tree, curve3.curve,1.5)
    assert(time_ints == {1: (0, 5), 9: (7, 9)})
    time_ints = get_sublevel_sets(births_only_merge_tree, curve3.curve,1.6)
    assert(time_ints == {1: (0, 9)})

    # find maxima
    curve4 = Curve(curve3.reflect())
    births_only_merge_tree = tmt.births_only(curve4.curve)
    time_ints = get_sublevel_sets(births_only_merge_tree, curve4.curve,0.5)
    assert(time_ints == {0: (0, 1), 5: (4, 8)})
    time_ints = get_sublevel_sets(births_only_merge_tree, curve4.curve,1.1)
    assert(time_ints == {5: (3, 9)})

    # curve 3 with 2 equal points
    curve5 = Curve({0:2,1:0,2:0,3:2,4:3,5:3,6:1.5,7:0})
    births_only_merge_tree = tmt.births_only(curve5.curve)
    time_ints = get_sublevel_sets(births_only_merge_tree, curve5.curve,0.5)
    assert(time_ints == {1: (0, 3), 7: (6, 7)})
    time_ints = get_sublevel_sets(births_only_merge_tree, curve5.curve,1.1)
    assert(time_ints == {1: (0, 4), 7: (5, 7)})
    time_ints = get_sublevel_sets(births_only_merge_tree, curve5.curve,1.5)
    assert(time_ints == {1: (0, 4), 7: (5, 7)})
    time_ints = get_sublevel_sets(births_only_merge_tree, curve5.curve,1.6)
    assert(time_ints == {1: (0, 7)})

    # constant curve
    curve6 = Curve({0:2,1:2,2:2,3:2,4:2,5:2,6:2,7:2})
    births_only_merge_tree = tmt.births_only(curve6.curve)
    time_ints = get_sublevel_sets(births_only_merge_tree, curve6.curve,0.5)
    assert(time_ints == {0: (0, 7)})
    print(time_ints)

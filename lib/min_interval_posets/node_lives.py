# The MIT License (MIT)
#
# Copyright (c) 2021 Robin Belton
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from min_interval_posets import triplet_merge_trees as tmt

def get_min_lives(curve):
    '''
    Calculates the node life for all the local minima in curve.
    :param births_only_merge_tree: merge tree dict with intermediate points removed
    :param curve: dict with times keying function values (should be of the form curve.curve or curve.normalized)
    :return: dict of node lives for each local minima in the curve
    '''
    births_only_merge_tree = tmt.births_only(curve)
    min_lives = dict()
    for u,(s,v) in births_only_merge_tree.items():
        if s == v:
            min_lives[u] = ((max(curve.values())-min(curve.values()))/2)
        else:
            min_lives[u] = (abs(curve[u]-curve[s])/2)
    return min_lives

def get_node_lives(curve):
    '''
    Calculates the node lives for all the local extrema in curve.
    :param curve: curve object
    :return: dict of node lives for each local extrema in the curve
    '''
    curve_max = Curve(curve.reflect())
    min_lives = get_min_lives(curve.curve)
    max_lives = get_min_lives(curve_max.curve)
    node_lives = {**min_lives, **max_lives}
    return(node_lives)

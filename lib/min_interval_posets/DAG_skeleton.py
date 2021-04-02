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

from min_interval_posets import eps_intersection as ei

def get_nodes(name, curve):
    '''
    For a given (named) curve find nodes of that curve
    :param name: A string uniquely identifying the curve
    :param curve: dict with float times keying float function values (should be of the form curve.curve or curve.normalized)
    :return: sorted list of tuples where first element is the time point of the extremum,
     second element is name + extremum type
    '''
    nodes = []
    for u in curve.keys():
        ex_type_u = ei.get_extremum_type(u, curve)
        if ex_type_u == "min" or ex_type_u == "max":
            nodes.append((u, (name, ex_type_u)))
    nodes.sort()
    return nodes

def get_DAGskeleton(curves):
    '''
    Construct DAG on multiple curves when eps = 0.
    :param curves: dict of instances of Curve, each keyed by unique name
    :return: DAG of curves at eps = 0.
    '''
    nodes = []
    edges = []

    for name, curve in curves.items():
        curve_nodes = get_nodes(name, curve.curve)
        N = len(nodes)
        nodes.extend(curve_nodes)
    edges = [(i,j) for i in range(len(nodes)) for j in range(len(nodes)) if nodes[i][0] < nodes[j][0]]

    return nodes, edges

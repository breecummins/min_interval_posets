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

from min_interval_posets import DAG_skeleton as ds
from min_interval_posets import node_lives as nl
from min_interval_posets import eps_intersection as ei

def get_extremalDAG(curves):
    '''
    Computes the extremal DAG for a set of discrete functions
    :param curve: dict with times keying function values (Curve.curve or Curve.normalized)
    :return: a list with time points, labels, and edges with weights. The nodes
    in the edge are indicated by index values.
    '''
    # computing and organizing extremal DAG skeleton (i.e. no node or edge weights)
    DAG = ds.get_DAGskeleton(curves)
    times = [DAG[0][i][0] for i in range(len(DAG[0]))]
    labels = [DAG[0][i][1][0] for i in range(len(DAG[0]))]
    nodes = [DAG[0][i][1] for i in range(len(DAG[0]))]
    edges = DAG[1]
    edge_weights = []
    node_weights = []

    # this loop goes through and computes the node weights
    for key in curves.keys():
        node_lives = nl.get_node_lives(curves[key])
        for i in range(len(times)):
            if labels[i] == key:
                node_weights.append((i, node_lives[times[i]]))

    # this loop goes through and computes the edge weights
    for u,v in edges:
        if labels[u] == labels[v]: # if nodes are part of same curve, then compute min of node lives
            edge_weights.append(((u,v), min(node_weights[u][1], node_weights[v][1])))
        else: # if nodes are from different curves, then compute min of node lives and eps intersection value
            edge_weights.append(((u,v), min(ei.get_eps_intersection(times[u],times[v],curves[labels[u]],curves[labels[v]]),
                                 node_weights[u][1], node_weights[v][1])))

    return nodes, node_weights, edge_weights

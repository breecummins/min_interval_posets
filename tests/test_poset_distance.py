# The MIT License (MIT)
#
# Copyright (c) 2018 Riley Nerem
#
# Edited by Bree Cummins
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

import networkx as nx
import numpy as np
import random
from ..libposets import poset_distance as ldag

def random_graph(N,Nlabels,edge_p):
    G = nx.DiGraph()
    rand = np.random.rand(N,N)
    Gmatrix = (rand <edge_p)
    Gmatrix[np.tril_indices(N)] = 0
    G = nx.convert_matrix.from_numpy_matrix(Gmatrix,create_using=G)
    for n in G.nodes:
        G.nodes[n]['label'] = str(random.choice(range(0,Nlabels,1)))
    return(G)

def benchmark(N,n,Nlabels,edge_p=0.25,seed=0):
    np.random.seed(seed)
    G = random_graph(N,Nlabels,edge_p)
    H = random_graph(N,Nlabels,edge_p)
    for i in range(n):
        print(ldag.dag_distance(G,H))

def example1():
    G = nx.DiGraph()
    G.add_nodes_from(range(1,11,1))
    G.add_edges_from([(1,2),(2,3),(4,5),(5,6),(6,7),(8,9),(9,10),(1,5),(5,3),(8,5),(10,3)])
    nx.set_node_attributes(G,{1:'xmax',2:'xmin',3:'xmax',4:'ymax',5:'ymin',6:'ymax',7:'ymin',8:'zmin',9:'zmax',10:'zmin'},'label')
    H = nx.DiGraph()
    H.add_nodes_from(range(1,7,1))
    H.add_edges_from([(1,2),(2,3),(4,5),(5,6),(4,2),(2,6)])
    nx.set_node_attributes(H,{1:'xmax',2:'xmin',3:'xmax',4:'ymin',5:'ymax',6:'ymin'},'label')
    return(G,H)


def example2():
    G = nx.DiGraph()
    G.add_nodes_from(range(1,7,1))
    G.add_edges_from([(1,2),(1,4), (3,4), (5,4), (5,6)])
    nx.set_node_attributes(G,{1:'xmin',2:'xmax',3:'ymin',4:'ymax',5:'zmax',6:'zmin'},'label')
    H = nx.DiGraph()
    H.add_nodes_from(range(1,7,1))
    H.add_edges_from([(1,2),(1,3),(3,4),(5,4),(5,6)])
    nx.set_node_attributes(H,{1:'xmin',2:'xmax',3:'ymax',4:'ymin',5:'zmin',6:'zmax'},'label')
    return(G,H)

def example3():
    G = nx.DiGraph()
    G.add_nodes_from(range(1,10,1))
    G.add_edges_from([(1,2),(2,3), (3,4), (4,5), (6,7),(7,8),(7,1),(8,5)])
    nx.set_node_attributes(G,{1:'xmin',2:'xmax',3:'xmin',4:'xmax',5:'xmin',6:'ymin',7:'ymax',8:'ymin',9:'zmin'},'label')
    H = nx.DiGraph()
    H.add_nodes_from(range(1,8,1))
    H.add_edges_from([(1,2),(2,3),(4,5),(5,6),(4,3),(2,5)])
    nx.set_node_attributes(H,{1:'xmax',2:'xmin',3:'xmax',4:'ymax',5:'ymin',6:'ymax',7:'zmax'},'label')
    return(G,H)

def test_dag():
    G,H = example1()
    assert ldag.getmaxcommonsubgraphsize(G,H) == 14
    assert ldag.dag_distance(G,H) == 21
    G,H = example2()
    assert ldag.getmaxcommonsubgraphsize(G,H) == 8
    assert ldag.dag_distance(G,H) == 7
    G,H = example3()
    assert ldag.getmaxcommonsubgraphsize(G,H) == 10
    assert ldag.dag_distance(G,H) == 31

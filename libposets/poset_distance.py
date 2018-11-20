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


def dag_distance(G,H):
    '''
    G and H are nx.DiGraph objects with node labels, representing ACYCLIC graphs. 
    Returns the distance between G and H.
    '''
    G = nx.transitive_closure(G)
    H = nx.transitive_closure(H)
    return len(G.nodes) + len(H.nodes) + len(G.edges) + len(H.edges) - 2*getmaxcommonsubgraphsize(G,H)


def makematchinggraph(G,H):
    # G and H are digraphs, matching_graph is undirected
    matching_graph = nx.Graph()
    for i in G.nodes():
        for j in H.nodes():
            if G.nodes[i]['label'] == H.nodes[j]['label']:
                matching_graph.add_node((i,j))
    for p in matching_graph.nodes():
        for q in matching_graph.nodes():
            if G.has_edge(p[0],q[0]) and H.has_edge(p[1],q[1]):
                matching_graph.add_edge(p,q)
    return matching_graph


def node_in(N,node_dict):
    for n in node_dict:
        if N == n[1]:
            return(True)
    return False


def num_edges(node_dict):
    return sum([sum([(ne in node_dict) for ne in node_dict[node]]) for node in node_dict])/2


def find_num_nodes(G,H):
    label_dict_g = {}
    label_dict_h = {}
    for ng in G.nodes:
        if G.nodes[ng]['label'] not in label_dict_g:
            label_dict_g[G.nodes[ng]['label']] = 1
        else:
            label_dict_g[G.nodes[ng]['label']] += 1
    for nh in H.nodes:
            if H.nodes[nh]['label'] not in label_dict_h:
                label_dict_h[H.nodes[nh]['label']] = 1
            else:
                label_dict_h[H.nodes[nh]['label']] += 1
    tot_n = 0
    for label in label_dict_g:
        if label in label_dict_h:
            tot_n+= min(label_dict_g[label],label_dict_h[label])
    return tot_n


def getmaxcommonsubgraphsize(G,H):
    numnodes = find_num_nodes(G,H)
    G = nx.transitive_closure(G)
    H = nx.transitive_closure(H)
    matching_graph = makematchinggraph(G,H)
    labels = [v for v in matching_graph.nodes()]
    mg_nodes = dict([(n, [e for e in matching_graph.neighbors(n)]) for n in matching_graph])
    Gn,Hn = zip(*labels)
    def pick_nodes(G_list, node_dict):
        if len(G_list) == 0:
                return(numnodes+num_edges(node_dict))
        sizes = 0
        for node in mg_nodes:
            if node[0] == G_list[0] and not node_in(node[1], node_dict):
                #check if node in matching graph corresponds to our node in G and check if node choice is valid
                sizes=max(sizes,pick_nodes(G_list[1:], {**node_dict,node:mg_nodes[node]}))
                #pick this node and then make recursive call to pick other nodes
        if numnodes < len(node_dict) + len(G_list):
            sizes = max(sizes, pick_nodes(G_list[1:], node_dict))
        #Check the case in which no node in the mathcing graph corrisponds to G_list[0]
        return(sizes)
    #Gn is the list of nodes in G, for each node in G we must pick a node in the matching graph.
    return pick_nodes(list(set(Gn)),{})


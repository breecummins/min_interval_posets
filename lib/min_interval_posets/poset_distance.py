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


def normalized_dag_distance(G,H):
    return dag_distance(G,H) / (len(G.nodes) + len(H.nodes) + len(G.edges) + len(H.edges))


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
    lab_count = {}
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
            lab_count[label] = min(label_dict_g[label],label_dict_h[label])
            tot_n+= lab_count[label]
    for label in label_dict_h:
        if label not in label_dict_g:
            lab_count[label] = 0
    return tot_n, lab_count




def getmaxcommonsubgraphsize(G,H):
    numnodes, fin_count = find_num_nodes(G,H)
    end_count = {}
    start_count = {}
    for lab in fin_count:
        end_count[lab] = 0
        start_count[lab] = 0
    for lab in fin_count:
        for node in G.nodes:
            if G.nodes[node]['label'] == lab:
                start_count[lab] +=1
    G = nx.transitive_closure(G)
    H = nx.transitive_closure(H)
    matching_graph = makematchinggraph(G,H)
    labels = [v for v in matching_graph.nodes()]
    mg_nodes = dict([(n, [e for e in matching_graph.neighbors(n)]) for n in matching_graph])
    Gn,Hn = zip(*labels)
    def pick_nodes(G_list, node_dict, s_count, e_count):
        if len(G_list) == 0:
                return(numnodes+num_edges(node_dict))
        sizes = 0
        l = G.nodes[G_list[0]]['label']
        s_count[l] += -1
        e_count[l] += 1
        pre = [n for n in G.predecessors(G_list[0])]
        psi_of_pre = [node[1] for node in node_dict if (node[0] in pre and l == G.nodes[node[0]]['label'])]
        not_valid = []
        for n in psi_of_pre:
            not_valid+= [n for n in H.predecessors(n)]
        not_valid = set(not_valid)
        for node in mg_nodes:
            if node[0] == G_list[0] and not node_in(node[1], node_dict) and node[1] not in not_valid:
                #check if node in matching graph corresponds to our node in G and check if node choice is valid

                sizes=max(sizes,pick_nodes(G_list[1:], {**node_dict,node:mg_nodes[node]}, s_count.copy(),e_count.copy()))
                #pick this node and then make recursive call to pick other nodes
        if fin_count[l] < e_count[l] + s_count[l]:
            e_count[l]+= -1
            sizes = max(sizes, pick_nodes(G_list[1:], node_dict, s_count.copy(), e_count.copy()))
        #Check the case in which no node in the mathcing graph corrisponds to G_list[0]
        return(sizes)
    #Gn is the list of nodes in G, for each node in G we must pick a node in the matching graph.
    return pick_nodes(list(set(Gn)),{}, start_count,end_count)


def poset_to_nx_graph(poset):
    names,edges = poset
    G = nx.DiGraph()
    for k,n in enumerate(names):
        G.add_node(k,label=str(n))
    G.add_edges_from(edges)
    return G

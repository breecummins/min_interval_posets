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
    return 1 - getmaxcommonsubgraphsize(G,H)/(max(len(G.edges), len(H.edges)))

normalized_dag_distance = dag_distance

def makematchinggraph(G,H):
    # G and H are digraphs, matching_graph is undirected
    matching_graph = nx.Graph()
    for i in G.nodes():
        for j in H.nodes():
            if G.nodes[i]['label'] == H.nodes[j]['label']:
                matching_graph.add_node((i,j))
                matching_graph.nodes[(i,j)]['label'] = G.nodes[i]['label']
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


def num_edges(node_dict,nodes):
    return sum([sum([(ne in nodes) for ne in node_dict[node]]) for node in nodes])/2


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
        else:
            lab_count[label] = 0
    for label in label_dict_h:
        if label not in label_dict_g:
            lab_count[label] = 0
    return lab_count


def make_node_dic(G):
    dic = {}
    labels = set([G.nodes[n]['label'] for n in G.nodes])
    for l in labels:
       dic[l] = [n for n in G.nodes if G.nodes[n]['label'] == l]
    return(dic)

def getmaxcommonsubgraphsize(G,H):
    G = nx.transitive_closure(G)
    H = nx.transitive_closure(H)
    #Calculate number of nodes of each label in the MCES. (We only consider solutions with a maximal number of nodes)
    #fin_count is a dictionary of number of nodes keyed by label
    fin_count = find_num_nodes(G,H)
    #end_count will keep track of how many nodes of each label have been matched so far
    end_count = {lab:0 for lab in fin_count}
    #G_count will keep track of how many nodes of each label in g have yet to be matched
    G_count = {lab:0 for lab in fin_count}
    #Populate G_count
    for lab in fin_count:
        for node in G.nodes:
            if G.nodes[node]['label'] == lab:
                G_count[lab] +=1
    matching_graph = makematchinggraph(G,H)
    mg_nodes_list = list(matching_graph.nodes())
    if len(mg_nodes_list) == 0:
        return 0
    #mg_nodes is a dictionary keyed by matching graph node which gives edges connected to a node
    mg_nodes = {n: [e for e in matching_graph.neighbors(n)] for n in matching_graph}
    Gn,Hn = zip(*mg_nodes_list)
    S = G.subgraph(Gn)
    #Gl is the list of nodes in G and Hs is the set of nodes in H
    #The order of elements of Gl respects the partial order given by G
    Gl = list(nx.topological_sort(S))
    Hs = set(Hn)
    #G_list is unmatched nodes in G
    #matches is the set of ordered pairs which match nodes from G to H, thus it is a list of nodes in the mathcing graph
    #g_count tracks the number of nodes of each label in G_list
    #g_count tracks the number of nodes of each label in matches
    def pick_nodes(G_list, matches, g_count,  e_count, Hs):
        #Base case: when there are no nodes left in G to match
        if len(G_list) == 0:
            #Calculate the number of edges in this common edge subgraph
            return(num_edges(mg_nodes, matches))
        sizes = 0
        #the function will try to find a match for the next item in G_list, this is node_to_match
        node_to_match = G_list[0]
        #l is the label of node_to_match
        l = G.nodes[node_to_match]['label']
        #change counts since one node is removed from G_list and one added to nodes
        g_count[l] += -1
        e_count[l] += 1
        #each h_node (node in H with label l) is a potential match
        for h_node in Hs[l]:
            new_match   = (node_to_match, h_node)
            #no_pair gives the nodes in H which can not have a pair if new_match is used. Here we use that G_list respects the partial order
            no_pair = [h for h in H.predecessors(h_node) if  h  in Hs[l]]
            #check if the above restriction allows the correct final number of nodes of each label to be reached.
            if (fin_count[l] <= len(Hs[l])+ e_count[l] - len(no_pair) -1):
                #copy Hs to new_Hs#
                new_Hs = {l:Hs[l].copy() for l in Hs}
                new_Hs[l].remove(h_node)
                for m in no_pair:
                    new_Hs[l].remove(m)
                sizes=max(sizes,pick_nodes(G_list[1:], matches|{new_match}, g_count.copy(),e_count.copy(), new_Hs))
        #determine if not matching node_to_match to any node in H can result in a graph with the correct number of nodes of each label
        if fin_count[l] < e_count[l] + g_count[l]:
            e_count[l]+= -1
            #this is the case where node_to_match is not matched
            sizes = max(sizes, pick_nodes(G_list[1:], matches, g_count.copy(), e_count.copy(), Hs.copy()))
        return(sizes)
    #initial recursive call
    return pick_nodes(Gl,set(), G_count.copy(), end_count.copy(), make_node_dic(H))

def poset_to_nx_graph(poset):
    names,edges = poset
    G = nx.DiGraph()
    for k,n in enumerate(names):
        G.add_node(k,label=str(n))
    G.add_edges_from(edges)
    return G

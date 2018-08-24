from libposets.curve import Curve
import libposets.posets as po
import networkx as nx
import itertools

def graphsize(G):
    return len(G.nodes()) + len(G.edges())

def makematchinggraph(G,H):
    # G and H are digraphs, matching_graph is undirected
    matching_graph = nx.Graph()
    for i in G.nodes():
        for j in H.nodes():
            if i.label() == j.label():
                matching_graph.add_node(label=str((i,j)))
    for v in matching_graph.nodes():
        p = eval(v.label())
        for w in matching_graph.nodes():
            q =  eval(w.label())
            if G.has_edge(p[0],q[0]) and H.has_edge(p[1],q[1]):
                matching_graph.add_edge(v,w)
    return matching_graph

def getmaxcommonsubgraphsize(G,H):
    mcs_size = 0
    matching_graph = makematchinggraph(G,H)
    labels = [eval(v.label()) for v in matching_graph.nodes()]
    Gn,Hn = zip(*labels)
    if len(Gn) == len(set(Gn)) and len(Hn) == len(set(Hn)):
        mcs_size = max(mcs_size,graphsize(matching_graph))
    else:
        # some nodes in G or H are repeated in the matching graph
        # have to remove them
        nodes = []
        for n in graph.nodes():
            if Gn.count(n[0]) > 1 or Hn.count(n[1]) > 1:
                nodes.append(n)
        # the following is not efficient, but is guaranteed to find the maximum
        # be careful of removing any of the steps (i.e., removing 2 nodes may give a larger
        # size than removing one if the two nodes remove fewer edges)
        for s in range(1,len(nodes)):
            for c in itertools.combinations(nodes,s):
                mg = matching_graph.copy()
                for v in c:
                    mg.remove_node(v)
                    mcs_size = max(mcs_size,graphsize(mg))
    return mcs_size

def pairwisedist(G,H):
    return graphsize(G) + graphsize(H) - 2*getmaxcommonsubgraphsize(G,H)

def transred(G):
    return nx.algorithms.dag.transitive_reduction(G)

def parsefile():
    pass

def makecurves():
    pass

def getsubset():
    pass

def makeposet():
    pass

def dorandom():
    pass

def dogood():
    pass

def dobad():
    pass

def test():
    poset1 = (["x max", "x min", "x max", "y min", "y max", "y min", "y max"],[(0,1),()])
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

import math

def diff(str1, str2, i, j):
    '''
    Cost function used for modified Edit distance/alignment.
    :param str1 & str2: list of pairs where the first component is a string and the second component is a float
    :param i & j: row and column index of alignment matrix used to find modified Edit distance
    :return cost of aligning str1[i-1] with str2[j-1]
    '''
    # If labels are the same, then we compute the difference in weights.
    if str1[i-1][0] == str2[j-1][0]:
        value = abs(str1[i-1][1]-str2[j-1][1])
    # If labels are not the same, then we make the value very high. We never want to align strings with different labels.
    else:
        value = 10000
    return(value)

def get_alignmentmat(str1, str2):
    '''
    Compute alignment matrix used in modified Edit distance/alignment.
    :param str1 & str2: list of pairs where the first entry is a string and the second entry is a float
    :return alignment matrix
    '''
    # Create a table to store results of subproblems
    mat = [[0 for x in range(len(str2)+1)] for x in range(len(str1)+1)]
    # Fill mat[][]
    for i in range(len(str1)+1):
        for j in range(len(str2)+1):
            if i == 0 and j == 0:
                mat[i][j] = 0
            # Fill in first row of mat to be the partial sum of weights in str2
            elif i == 0:
                mat[i][j] = mat[i][j-1]+str2[j-1][1]
            # Fill in first column of mat to be the partial sum of weights in str2
            elif j == 0:
                mat[i][j] = mat[i-1][j]+str1[i-1][1]
            # Fill in the remaining matrix using cost function. mat[i][j] is the minimum of:
            # mat[i][j-1] + cost of aligning the next node in string 2 with an insertion (i.e. weight of str2[j-1])
            # mat[i-1][j] + cost of aligning the next node in string 1 with an insertion (i.e. weight of str1[i-1])
            # mat[i-1][j-1] + cost of aligning the next node in string 1 with the next node in string 2,
                             # assuming labels are same (i.e., abs(str1[i-1]-str2[j-1])
            else:
                mat[i][j] = min(mat[i][j-1]+str2[j-1][1], mat[i-1][j]+str1[i-1][1], mat[i-1][j-1]+diff(str1, str2, i, j))
    return mat

def get_bestalignment_index(str1, str2):
    '''
    Compute optimal alignment of str1 and str2.
    :param str1 & str2: list of pairs where the first entry is a string and the second entry is a float
    :return list where first item is a list where each entry is of the form ('Label', (weight from str1, weight from str2)).
    The second item of the list is a list of indices of the form (i,j) that can be interpreted as str1[i] is aligned with str2[j].
    Note, if either i or j is 'None', then an insertion was made.
    '''
    mat = get_alignmentmat(str1, str2)
    optstr = []
    index = []
    i = len(mat)-1 # row index of mat
    j = len(mat[0])-1 # column index of mat
    k = len(str1)-1 # index of str1
    m = len(str2)-1 # index of str2
    while i > 0 and j > 0:
        if mat[i-1][j-1]+diff(str1, str2, i, j) == mat[i][j] and str1[k][0] == str2[m][0]:
            optstr.append((str1[k][0], (str1[k][1], str2[m][1]))) # Diagonal move - align node in str1 with node in str2 as long  as labels are the same
            index.append((k,m))
            k = k-1
            m = m-1
            i = i-1
            j = j-1
        elif mat[i-1][j]+str1[i-1][1] == mat[i][j]:
            optstr.append((str1[k][0], (str1[k][1], 0))) # Vertical move - align node in str1 with an insertion in str2
            index.append((k, 'None'))
            i = i-1
            k = k-1
        else: # Horizontal move - align node in str2 with an insertion in str1
            optstr.append((str2[m][0], (0, str2[m][1])))
            index.append(('None', m))
            j = j-1
            m = m-1
    if i == 0 and j > 0: # In first row of matrix but not first column
        while j > 0:
            optstr.append((str2[m][0], (0, str2[m][1]))) # Horizontal move
            index.append(('None', m))
            j = j-1
            m = m-1
    elif j == 0 and i > 0: # In first column of matrix but not first row
        while i > 0:
            optstr.append((str1[k][0], (str1[k][1], 0))) # Vertical move
            index.append((k, 'None'))
            k = k-1
            i = i-1
    optstr.reverse()
    index.reverse()
    return optstr, index

def get_node_strings(names, DAG): 
    '''
    Extract labels and nodeweights in order to compute node alignment.
    :param names: string of names corresponding to curves in DAG
    :param DAG: extremal DAG
    :return: two lists where the first list consists of indices where each index
    corresponds to a curve in the DAG, and the second list consists of nodes in each curve
    '''
    labels = DAG[0]
    node_weights = DAG[1]
    strings = []
    index = []
    for i in range(len(names)):
        str = []
        for j in range(len(labels)):
            if labels[j][0] == names[i]:
                str.append((labels[j][1], node_weights[j][1]))
                index.append(j)
        strings.append(str)
    return index, strings

def align_DAGnodes_index(names, DAG1, DAG2): 
    '''
    Compute optimal alignment of corresponding backbones in DAG1 and DAG2.
    :param names: a list of names for each of the curves in DAG1 and DAG2. NOTE: DAG1 and DAG2 have the same 
     names for the curves they are representing & names are in same order for DAG1 & DAG2
    :param DAG1 & DAG2: extremal DAGS
    :return Two lists. The first list is of aligned nodes with corresponding weights from the two DAGS.
    The second list consists of pairs of indices of which nodes in the DAGs the weights come from.
    Specifically the pairs are of the form (i,j) and is interpreted as node i in DAG1 is aligned with node j in DAG2. 
    If either i  or j is "None", then we have an empty node for the corresponding DAG
    '''
    strings1 = get_node_strings(names, DAG1)
    strings2 = get_node_strings(names, DAG2)
    aligned_nodes = []
    node_indices = []
    start1 = 0
    start2 = 0
    for i in range(len(strings1[1])): # strings1 and strings2 will be of the same length b/c DAGs have same number of curves
        string_indices = get_bestalignment_index(strings1[1][i],strings2[1][i])[1]
        aligned_nodes.append(get_bestalignment_index(strings1[1][i], strings2[1][i])[0])
        for j in range(len(aligned_nodes[i])):
            if aligned_nodes[i][j][1][0] != 0:
                index1 = start1+string_indices[j][0]
            else:
                index1 = "None"
            if aligned_nodes[i][j][1][1] != 0:
                index2 = start2+string_indices[j][1]
            else:
                index2 = "None"
            node_indices.append((index1, index2))
        start1 = start1+(len(strings1[1][i]))
        start2 = start2+(len(strings2[1][i]))
    return aligned_nodes, node_indices

def DAG_dist(supergraph):
    '''
    Computes distance between extremal DAGs using the supergraph
    param supergraph: A list of the form [(nodes, edges)]. nodes is a list of
    the form [(name, (nodeweight1, nodeweight2))] and edges is a list of the form
    [((u,v),(edgeweight1, edgeweight2))] returns the euclidean distance between
    vec1 and vec2 where vec1 is the vector of 1st component weights and vec2 is
    the vector of second component weights
    '''
    vec1 = [supergraph[0][i][1][0] for i in range(len(supergraph[0]))]+[supergraph[1][i][1][0] for i in range(len(supergraph[1]))]
    vec2 = [supergraph[0][i][1][1] for i in range(len(supergraph[0]))]+[supergraph[1][i][1][1] for i in range(len(supergraph[1]))]
    dist = math.sqrt(sum((u-v)**2 for u,v in zip(vec1, vec2)))
    return dist

def get_supergraph(names, DAG1, DAG2):
    '''
    Computes the supergraph between two DAGs
    param names: list of names of the curves corresponding to DAG1 and DAG2. Both DAGs must have the same names.
    param DAG1 and DAG2: two extremal DAGS, these should be the output of the get_extremalDAG function
    return: A list of the form [(nodes, edges)]. nodes is a list of
    the form [(name, (nodeweight1, nodeweight2))] and edges is a list of the form
    [((u,v),(edgeweight1, edgeweight2))]
    '''
    nodes_plus_index = align_DAGnodes_index(names, DAG1, DAG2)
    nodes = []
    for i in range(len(names)):
        for j in range(len(nodes_plus_index[0][i])):
            nodes.append(((names[i], nodes_plus_index[0][i][j][0]),nodes_plus_index[0][i][j][1]))
    node_pairs = [(node_a, node_b) for node_a in range(len(nodes)) for node_b in range(len(nodes)) if node_a != node_b]
    node_indices = nodes_plus_index[1]
    edges = []
    for u,v in node_pairs: # adding edge weights of edges in supergraph
        DAG1_edge = (node_indices[u][0], node_indices[v][0])
        DAG2_edge = (node_indices[u][1], node_indices[v][1])
        edge_weight1 = 0
        for x,y in DAG1[2]:
            if x[0] == DAG1_edge[0] and x[1] == DAG1_edge[1]:
                edge_weight1 = y
        edge_weight2 = 0
        for x,y in DAG2[2]:
            if x[0] == DAG2_edge[0] and x[1] == DAG2_edge[1]:
                edge_weight2 = y
        edges.append(((u,v), (edge_weight1, edge_weight2)))
    nonzero_edges = []
    for i in range(len(edges)): # removing edges where both weights are zero
        if edges[i][1][0] != 0 or edges[i][1][1] != 0:
            nonzero_edges.append(edges[i])
    dist = DAG_dist((nodes,nonzero_edges))
    return nodes, nonzero_edges, dist

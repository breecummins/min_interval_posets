import numpy as np
from min_interval_posets import supergraph as sg

def test1():
    # Insertions at ends
    str1 = [('m', .5), ('M', .75), ('m', .9), ('M', .3)]
    str2 = [('M', .25), ('m', .5), ('M', .7), ('m', .8)]
    mat = sg.get_alignmentmat(str1, str2)
    mat_round = [[round(mat[i][j],8) for j in range(len(mat[0]))] for i in range(len(mat))]
    assert(mat_round == [[0, 0.25, 0.75, 1.45, 2.25],
     [0.5, 0.75, 0.25, 0.95, 1.75],
     [1.25, 1.0, 1.0, 0.3, 1.1],
     [2.15, 1.9, 1.4, 1.2, 0.4],
     [2.45, 2.2, 1.7, 1.5, 0.7]])
    check_uniqueness = sg.check_bestalignments(str1, str2)
    assert(check_uniqueness == "unique optimal alignment")
    alignment = sg.get_bestalignment_index(str1, str2)
    assert(alignment == ([('M', (0, 0.25)),
    ('m', (0.5, 0.5)),
    ('M', (0.75, 0.7)),
    ('m', (0.9, 0.8)),
    ('M', (0.3, 0))],
    [('None', 0), (0, 1), (1, 2), (2, 3), (3, 'None')]))
    alignment_cost = sum((abs(alignment[0][i][1][0]-alignment[0][i][1][1])) for i in range(len(alignment[0])))
    assert(alignment_cost == mat[len(mat)-1][len(mat[0])-1])

def test2():
    # Insertions at beginning & strings are of different lengths
    # NOTE there are two optimal alignments in this example
    str1 = [('m', .5), ('M', .05), ('m', .6), ('M', .7), ('m',.3)]
    str2 = [('m', .4), ('M', .75), ('m', .33)]
    mat = sg.get_alignmentmat(str1, str2)
    mat_round = [[round(mat[i][j],8) for j in range(len(mat[0]))] for i in range(len(mat))]
    assert(mat_round == [[0, 0.4, 1.15, 1.48],
     [0.5, 0.1, 0.85, 1.18],
     [0.55, 0.15, 0.8, 1.13],
     [1.15, 0.75, 1.4, 1.07],
     [1.85, 1.45, 0.8, 1.13],
     [2.15, 1.75, 1.1, 0.83]])
    check_uniqueness = sg.check_bestalignments(str1, str2)
    assert(check_uniqueness == "multiple optimal alignments")
    alignment = sg.get_bestalignment_index(str1, str2)
    assert(alignment == ([('m', (0.5, 0)),
    ('M', (0.05, 0)),
    ('m', (0.6, 0.4)),
    ('M', (0.7, 0.75)),
    ('m', (0.3, 0.33))],
    [(0, 'None'), (1, 'None'), (2, 0), (3, 1), (4, 2)]))
    alignment_cost = sum((abs(alignment[0][i][1][0]-alignment[0][i][1][1])) for i in range(len(alignment[0])))
    assert(round(alignment_cost, 8) == round(mat[len(mat)-1][len(mat[0])-1],8))

def test3():
    # Insertions in middle of strings and strings are of different lengths
    str1 = [('m', .5), ('M', .05), ('m', .4), ('M', .7), ('m',.3)]
    str2 = [('m', .5), ('M', .75), ('m', .33)]
    mat = sg.get_alignmentmat(str1, str2)
    alignment = sg.get_bestalignment_index(str1, str2)
    assert(alignment == ([('m', (0.5, 0.5)),
    ('M', (0.05, 0)),
    ('m', (0.4, 0)),
    ('M', (0.7, 0.75)),
    ('m', (0.3, 0.33))],
    [(0, 0), (1, 'None'), (2, 'None'), (3, 1), (4, 2)]))
    alignment_cost = sum((abs(alignment[0][i][1][0]-alignment[0][i][1][1])) for i in range(len(alignment[0])))
    assert(alignment_cost == mat[len(mat)-1][len(mat[0])-1])

def test4():
    # No diagonal moves in traceback
    str1 = [('a', .5), ('b', .05), ('c', .6), ('d', .7), ('e',.3)]
    str2 = [('f', .4), ('g', .75), ('h', .33)]
    mat = sg.get_alignmentmat(str1, str2)
    alignment = sg.get_bestalignment_index(str1, str2)
    assert(alignment == ([('f', (0, 0.4)),
    ('g', (0, 0.75)),
    ('h', (0, 0.33)),
    ('a', (0.5, 0)),
    ('b', (0.05, 0)),
    ('c', (0.6, 0)),
    ('d', (0.7, 0)),
    ('e', (0.3, 0))],
    [('None', 0),
    ('None', 1),
    ('None', 2),
    (0, 'None'),
    (1, 'None'),
    (2, 'None'),
    (3, 'None'),
    (4, 'None')]))
    alignment_cost = sum((abs(alignment[0][i][1][0]-alignment[0][i][1][1])) for i in range(len(alignment[0])))
    assert(alignment_cost == mat[len(mat)-1][len(mat[0])-1])

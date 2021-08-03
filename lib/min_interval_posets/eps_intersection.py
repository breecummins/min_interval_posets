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

from min_interval_posets.curve import Curve
from min_interval_posets.triplet_merge_trees import births_only
from min_interval_posets.sublevel_sets import get_sublevel_sets_no_restriction as gssnr

def get_extremum_type(a, curve):
    '''
    Decides if a is a min or max or neither.
    :param curve: dict with times keying function values (should be of form Curve.curve or Curve.normalized)
    :param a: the x-coordinate of a point in curve
    :return: string equal to "min", "max", or "neither"
    '''
    times = sorted([k for k in curve])
    index_a = times.index(a)

    if index_a == 0: # case that a is the first endpoint
       if curve[a] < curve[times[index_a+1]]:
           extremum = 'min'
       elif curve[a] > curve[times[index_a+1]]:
           extremum = 'max'
       else:
           extremum = 'neither'
    elif index_a == len(times)-1: # case that a is the final endpoint
       if curve[a] < curve[times[index_a-1]]:
           extremum = 'min'
       elif curve[a] > curve[times[index_a-1]]:
           extremum = 'max'
       else:
           extremum = 'neither'
    else: # case that a is not an endpoint
        if curve[times[index_a-1]] < curve[a] and curve[a] > curve[times[index_a+1]]:
            extremum = 'max'
        elif curve[times[index_a-1]] > curve[a] and curve[a] < curve[times[index_a+1]]:
            extremum = 'min'
        else:
            extremum = 'neither'
    return extremum

def get_eps_sup(a, curve, eps):
    '''
    Computes epsilon support interval for a local extremum.
    :param curve: curve object
    :param eps: float threshold (noise level) For normalized curves, 0 < eps < 1.
    :param a: the x-coordinate of a point in curve
    :return: epsilon support interval if a is a local extremum, otherwise returns FALSE
    '''
    ex_type_a = get_extremum_type(a, curve.curve)
    if ex_type_a == 'min':
        births_only_merge_tree = births_only(curve.curve)
        eps_sup_a = gssnr(births_only_merge_tree, curve.curve, eps)
    elif ex_type_a == 'max':
        new_curve = Curve(curve.reflect())
        births_only_merge_tree = births_only(new_curve.curve)
        eps_sup_a = gssnr(births_only_merge_tree, new_curve.curve, eps)
    else:
        return False
    return eps_sup_a[a]

def intervals_intersect(a, b, curve_a, curve_b, eps):
    '''
    Decides if the two epsilon support intervals intersect
    :param curve_a, curve_b: curve object
    :param eps: float threshold (noise level). For normalized curves, 0 < eps < 1.
    :param a: the x-coordinate of a point in curve_a
    :param b: the x-coordinate of a point in curve_b
    :return: a boolean variable indicating if the two epsilon support intervals intersect or not
    '''
    eps_sup_a = get_eps_sup(a, curve_a, eps)
    eps_sup_b = get_eps_sup(b, curve_b, eps)
    if a <= b:
        if eps_sup_b[0] <= eps_sup_a[1]:
            return True
    if b < a:
        if eps_sup_a[0] <= eps_sup_b[1]:
            return True
    return False

def get_eps_jumps(a, curve):
    '''
    Finds epsilon values where the epsilon support intervals for an extremum change
    :param curve_a: dict with times keying function values (should be of the form Curve.curve or Curve.normalized)
    :param a: the x-coordinate of a point in curve_a
    :return: a list of epsilon values where the epsilon support interval for extremum, a, change
    '''
    # current_extreme records the function value where the level set is taken
    # for finding the epsilon support interval
    ex_type_a = get_extremum_type(a, curve)
    if ex_type_a == 'neither':
        return False # function returns false if input a is not a local extremum of curve_a
    times = sorted([k for k in curve])
    index_a = times.index(a)
    epsilons = [0]

    i = index_a-1 # goes through points that come before a and see if they will cause an epsilon jump
    if i > 0:
        current_extreme = curve[times[i]]
        epsilons.append((abs(curve[times[i]]-curve[a])/2))
        while i > 0:
            i -= 1
            if ex_type_a == 'min' and curve[times[i]] > current_extreme:
                epsilons.append((abs(curve[times[i]]-curve[a])/2))
                current_extreme = curve[times[i]]
            elif ex_type_a == 'max' and curve[times[i]] < current_extreme:
                epsilons.append((abs(curve[times[i]]-curve[a])/2))
                current_extreme = curve[times[i]]

    i = index_a+1 # goes through points that come after a and see if they will cause an epsilon jump
    if i < len(times)-1:
        current_extreme = curve[times[i]]
        epsilons.append((abs(curve[times[i]]-curve[a])/2))
        while i < len(times)-1:
            i += 1
            if ex_type_a == 'min' and curve[times[i]] > current_extreme:
                epsilons.append((abs(curve[times[i]]-curve[a])/2))
                current_extreme = curve[times[i]]
            elif ex_type_a == 'max' and curve[times[i]] < current_extreme:
                epsilons.append((abs(curve[times[i]]-curve[a])/2))
                current_extreme = curve[times[i]]

    epsilons.sort()
    return epsilons

def get_eps_intersection(a, b, curve_a, curve_b):
    '''
    Finds smallest epsilon value for when the two epsilon intervals intersect
    :param curve: dict with times keying function values (Curve.curve or Curve.normalized)
    :param a: the x-coordinate of a point in curve_a
    :param b: the x-coordinate of a point in curve_b
    :return: a float indicating the smallest epsilon value for when the two epsilon intervals intersect
    '''
    eps_jumps_a = get_eps_jumps(a, curve_a.curve)
    eps_jumps_b = get_eps_jumps(b, curve_b.curve)
    epsilons = eps_jumps_a + eps_jumps_b
    epsilons.sort()

    for i in range(len(epsilons)):
        if intervals_intersect(a, b, curve_a, curve_b, epsilons[i]+1E-10) == True:
            return epsilons[i]

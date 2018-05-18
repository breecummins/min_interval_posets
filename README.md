Python 3 library to find the ɛ-minimum intervals for a time series and create a poset of the ɛ-minimal intervals for a collection of time series.

Dependencies:
numpy

To run tests, from the command line do

$ cd min_interval_posets  
$ pytest  

To create the figure and tables in the Example section of "Sequencing of extremal events in a noisy time series" (2018), from the command line do

$ cd min_interval_posets  
$ python scripts/figure_and_tables_2018.py

To find the ɛ-minimum intervals for a time series, first create a curve.Curve() object. Assume T is a vector of times, F is a vector of function values, and eps is a noise level.

ipython >> from libposets.curve import Curve

ipython >> import libposets.triplet_merge_trees as tmt

ipython >> import libposets.sublevel_sets as ss

ipython >> c = Curve({ t : v for (t,v) in zip(T,F) })

ipython >> births_only_merge_tree = tmt.births_only(c)

ipython >> time_ints = ss.minimal_time_ints(births_only_merge_tree, c, eps)

To find the ɛ-maximum intervals on the curve, run the same commands on the following Curve object.

ipython >> cmax = c.reflect()

To make a partial order of the ɛ-extremal intervals for two time series Curve objects at three different epsilon values, do the following. 

ipython >> from libposets import posets

ipython >> P = posets.main({"y":curvey,"z":curvez},[eps1, eps2, eps3])

The output is a list of tuples in the form (eps, poset), where each poset is a directed acyclic graph with nodes that are labeled by the curve name and whether they are a max or a min.
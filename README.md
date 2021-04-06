Python 3 library to find the ɛ-minimum intervals for a time series and create a poset of the ɛ-minimal intervals for a collection of time series.

Installation is locally via pip. In the command line, do
```bash
$ cd min_interval_posets
$ . install.sh

```


To run tests, from the command line do

```bash
$ cd min_interval_posets  
$ pytest 

``` 

To create the figure and tables in the Example section of "Using extremal events to characterize noisy time series" Berry et al. (2019), see the "Berry" Jupyter notebooks in the `scripts` folder.

To find the ɛ-minimal intervals for a time series, first create a curve.Curve() object. Assume T is a vector of times, F is a vector of function values, and eps is a noise level.

```bash
ipython >> from min_interval_posets.curve import Curve

ipython >> import min_interval_posets.triplet_merge_trees as tmt

ipython >> import min_interval_posets.sublevel_sets as ss

ipython >> c = Curve({ t : v for (t,v) in zip(T,F) })

ipython >> births_only_merge_tree = tmt.births_only(c.curve)

ipython >> time_ints = ss.get_sublevel_sets(births_only_merge_tree, c.curve, eps)

```

To find the ɛ-maximal intervals on the curve, run the same commands on the following Curve object.

```bash
ipython >> cmax = Curve(c.reflect())

```

To make a partial order of the ɛ-extremal intervals for two time series Curve objects `cy` and `cz` at three different epsilon values, do the following. 

```bash
ipython >> from min_interval_posets.posets import eps_posets

ipython >> P = eps_posets({"y":cy,"z":cz},[eps1, eps2, eps3])

```

The output is a list of tuples in the form (eps, poset), where each poset is a directed acyclic graph with nodes that are labeled by the curve name and whether they are a max or a min.

To calculate the distance between two posets `p` and `q`, where `P = [(eps,p)]` and `Q = [(eps,q)]` are outputs of `eps_posets`, do
```bash
ipython >> import min_interval_posets.poset_distance as pd

ipython >> graph_p = pd.poset_to_nx_graph(p)

ipython >> graph_q = pd.poset_to_nx_graph(q)

ipython >> dist = pd.dag_distance(graph_p,graph_q)

```
Let `curves ` be a dictionary where the keys are names of the curves and the items are curve classes (ASK: or curve objects?). To compute the extremal DAG for `curves`, do
```bash 
ipython >> from min_interval_posets.DAG_skeleton import get_DAGskeleton

ipython >> from min_interval_posets.node_lives import get_node_lives

ipython >> from min_interval_posets.eps_intersection import get_eps_intersection

ipython >> from min_interval_posets.extremal_DAG import get_extremalDAG

ipython >> extremalDAG = get_extremalDAG(curves)

```
Let `DAG1` and `DAG2` be two extremal DAGs that have the same data structure as the output of the `get_extremalDAG` function. Additionally, suppose `DAG1` and `DAG2` have the same 
names for the curves they are representing and the names are in same order for `DAG1` and `DAG2`.
Let `names` be a list of the named curves in the same order as the curve names in `DAG1` and `DAG2`. To compute the supergraph of `DAG1` and `DAG2`, do
```bash
ipython >> import math

ipython >> supergraph = get_supergraph(names, DAG1, DAG2)
```

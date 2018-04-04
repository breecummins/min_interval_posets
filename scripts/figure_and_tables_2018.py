import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams.update({'font.size': 22})
from libposets.curve import Curve
import libposets.triplet_merge_trees as tmt
import libposets.sublevel_sets as ss

# call from containing folder:
# python3 scripts/figures_and_tables_2018.py
# to create the figure and tables found in
# "Comparing timing of extremal events in collection of noisy time series" (2018)

# make curves
x = np.arange(-2.5,5.01,0.01)
y = 0.15*x**4 - 0.32*x**3 - 1.305*x**2 +0.27*x
np.random.seed(0)
eta = np.random.normal(0,0.25,x.shape)
z = y+eta

# make Figure
plt.plot(x,z,linewidth=2)
plt.plot(x,y,linewidth=1.25,color="red",zorder=10)
plt.savefig("noisy_curve.pdf",format = "pdf")

# make Tables
epsilons = [0.25,0.5,0.75,1.0,1.55, 2.33]

def make_table_values(curve,time,label="minima"):
    births_only_merge_tree = tmt.births_only(curve)
    mins=[]
    ints=[]
    for eps in epsilons:
        time_ints = ss.minimal_time_ints(births_only_merge_tree, curve, eps)
        mins.append(len(time_ints))
        ints.append(time_ints[time])
    print("Eps  # {}  int at x={}".format(label,time))
    for (a,b,c) in zip(epsilons,mins,ints):
        print(("    ".join(["{:.2f}".format(a),str(b),str(c)])))

print("Smooth curve: minima")
smooth_curve = Curve({ round(t,2) : round(v,10) for (t,v) in zip(x,y) })
time = 3.0
make_table_values(smooth_curve.curve,time,"minima")

print("\n\nNoisy curve: minima")
noisy_curve = Curve({ round(t,2) : round(v,10) for (t,v) in zip(x,z) })
time = 2.97
make_table_values(noisy_curve.curve,time,"minima")

print("\n\nSmooth curve: maxima")
time = 5.0
make_table_values(smooth_curve.reflect(),time,"maxima")

print("\n\nNoisy curve: maxima")
time = 5.0
make_table_values(noisy_curve.reflect(),time,"maxima")




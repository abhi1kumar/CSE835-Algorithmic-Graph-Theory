
import os, sys
sys.path.append(os.getcwd())

import numpy as np
from pg import *

# This is the 61st graph
graph_dict= {0 : {5:1, 6:1, 7:1}, 1 : {5:1, 6:1, 7:1}, 2 : {3:1, 4:1, 7:1}, 3 : {2:1, 4:1, 7:1}, 4 : {2:1, 3:1, 7:1}, 5 : {0:1, 1:1, 6:1}, 6 : {0:1, 1:1, 5:1, 7:1}, 7 : {0:1, 1:1, 2:1, 3:1, 4:1, 6:1}}
g            = Graph(graph_dict)
st           = g.spanning_trees_count()
deg_seq      = np.array(g.degree_sequence())
 
g_comp       = g.complement()
st_comp      = g_comp.spanning_trees_count()
deg_seq_comp = np.array(g_comp.degree_sequence())


print("G dict")
print(graph_dict)

# Quick Sanity Check
if np.any(deg_seq == deg_seq_comp):
    print("\nDegree sequence of the complement is not the same. So g is definitely not self-complementary\n")
else:
    print("Degree sequence is same. CHECK the graph yourself")

print("#Spanning trees(G)           = {}".format(st))
print("#Spanning trees(G_complement)= {}".format(st_comp))

g     .draw_matplotlib(layout= "circular", path= "images/fig_5_4.png")
g_comp.draw_matplotlib(layout= "circular", path= "images/fig_5_4_compl.png")

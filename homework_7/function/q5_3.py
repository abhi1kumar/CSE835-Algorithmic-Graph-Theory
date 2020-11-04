
import os, sys
sys.path.append(os.getcwd())

from pg import *

n= 6
q= 10
c= 1 # connected graphs 

# Generate all connected graphs
all_graphs = gen_nq_graphs(n, q, c= c)
num_graphs = len(all_graphs)

print("{} graphs found".format(num_graphs))

# Search for the graph with maximum spanning trees
max_num_st = -1
max_index  = -1
for i in range(num_graphs):
    g      = Graph(all_graphs[i])
    num_st = g.spanning_trees_count()

    if num_st >  max_num_st:
        max_num_st = num_st
        max_index  = i

max_dict = all_graphs[max_index]
g = Graph(max_dict)
print(max_dict)
print("Max num of spanning trees = {} for graph {}".format(max_num_st, max_index))

print(g.edges())
g.draw_matplotlib(layout= "circular", path= "images/fig_5_3.png")

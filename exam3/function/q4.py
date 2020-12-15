

import os, sys
sys.path.append(os.getcwd())

from pg import *

g =  Graph({0: {7: 7, 5: 7, 3: 1}, 1: {6: 3, 5: 1, 7: 5}, 2: {7: 4, 5: 4, 4: 8},\
            3: {6: 8, 4: 8, 0: 1}, 4: {2: 8, 3: 8, 6: 7}, 5: {0: 7, 2: 4, 1: 1},\
            6: {1: 3, 3: 8, 4: 7}, 7: {0: 7, 2: 4, 1: 5}})

#g.draw_matplotlib(vertex_size= 1500, show_figure= True)

#Get all spanning trees of a graph
all_trees      = g.spanning_trees_all()

min_delay_cost = 100000000
tree_index     = -1
for i in range(len(all_trees)):
    curr_cost = Graph(all_trees[i]).delay_cost()
    if curr_cost < min_delay_cost:
        min_delay_cost = curr_cost
        tree_index     = i

print("Min Delay Spanning Tree Delay Cost = {}".format(min_delay_cost))

#Get the center vertex
center = g.center()[1]
print("Center Vertex= {}".format(center))

#Get the distance preserving tree with edge weights
dp_tree = g.dpt(source= center)

"""
#Get the distance preserving tree with all edge weights 1
dp_tree = g.dpTreeGraph(v= center)

#Update the weights to the original graph
dp_tree_edges = dp_tree.edges()

for i in range(len(dp_tree_edges)):
    edge             = dp_tree_edges[i]
    u                = edge[0]
    v                = edge[1]
    edge_wt_original = g.edge_weight(u, v)
    dp_tree.change_edge_weight(edge, edge_wt_original)

"""
dp_tree.draw_matplotlib()#vertex_size= 1500, show_figure= True)

print("Distance Preserving Tree Delay Cost= {}".format(dp_tree.delay_cost()))

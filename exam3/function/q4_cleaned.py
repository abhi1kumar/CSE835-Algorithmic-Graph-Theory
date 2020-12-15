

import os, sys
sys.path.append(os.getcwd())

from pg import *

g =  Graph({0: {7: 7, 5: 7, 3: 1}, 1: {6: 3, 5: 1, 7: 5}, 2: {7: 4, 5: 4, 4: 8}, 3: {6: 8, 4: 8, 0: 1}, 4: {2: 8, 3: 8, 6: 7}, 5: {0: 7, 2: 4, 1: 1}, 6: {1: 3, 3: 8, 4: 7}, 7: {0: 7, 2: 4, 1: 5}})

#Get the center vertex
center = g.center()[1]
print("Center Vertex= {}".format(center))

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

dp_tree.draw_matplotlib()

print("Distance Preserving Tree Delay Cost= {}".format(dp_tree.delay_cost()))



import os, sys
sys.path.append(os.getcwd())

from pg import *

def display_result(result, string="", new_line= True):
    if new_line:
        print("")

    if biparticity[0] == 1:
        print(string)
    else:
        print("Not" + string)


g =  Graph({0:  {1: 1, 8: 1, 14: 1}, 
            1:  {0: 1, 2 : 1, 4: 1}, 2: { 1: 1,  3: 1,  5: 1},  3: {2: 1,  4: 1, 6: 1}, 
            4:  {1: 1, 3 : 1, 5: 1}, 5: { 2: 1,  4: 1,  6: 1},  6: {3: 1,  5: 1, 7: 1}, 
            7:  {6: 1, 13: 1,19: 1}, 
            8:  {0: 1, 9: 1, 11: 1}, 9: { 8: 1, 10: 1, 12: 1}, 10: {9: 1, 11: 1, 13: 1},
            11: {8: 1, 10: 1,12: 1},12: { 9: 1, 11: 1, 13: 1}, 13: {10:1, 12: 1, 7: 1},
            14: {0: 1, 15: 1,17: 1},15: {14: 1, 16: 1, 18: 1}, 16: {15:1, 17: 1, 19: 1},
            17:{14: 1, 16: 1,18: 1},18: {15: 1, 17: 1, 19: 1}, 19: { 7:1, 16: 1, 18: 1},
})
#g.draw_matplotlib(vertex_size= 600, show_figure= True)

#Biparticity
biparticity = g.biparticity()
display_result(result=biparticity[0], string="Bipartite")
print(biparticity[1], biparticity[2])

# Eulerian
display_result(result=g.eulerian(), string="Eulerian")

#Diameter
print("Diameter= {}".format(g.diameter()))

#Central Vertices
print("Center  = {}".format(g.center()[1]))

#Blocks

#Girth
print("Girth   = {}".format(g.girth()[0]))

#Lambda

#Kappa

#Max matching set 
print("Max matching set   = {}".format(g.matching()))

#Max independent set 
print("Max independent set= {}".format(g.max_independent_set()))

#Min covering set = |V(G)| - Max independent set
print("Min covering       = {}".format(g.order()-g.max_independent_set()[0]))

#Min dominating set
#print("Min Dominating set= {}".format(g.order()-g.matching()[0]))

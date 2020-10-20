
import os, sys
sys.path.append(os.getcwd())

from pg import *

print("Cube")
g = cube(3)
g.draw_matplotlib(layout= "circular", vertex_size= 700, fs= 12, lw= 2, path= "images/fig_3_8.png")
print("Least number of edges = {}".format(g.make_dh()))

g.add_edge(0, 7, 1)
g.add_edge(1, 6, 1)
g.add_edge(2, 5, 1)
print(g.edges())
print("DH = {}".format(g.distance_hereditary(print_nodes= True)))


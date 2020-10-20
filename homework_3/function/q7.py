
import os, sys
sys.path.append(os.getcwd())

from pg import *

print("Petersen Graph")
g = petersen_graph()
#g.draw_matplotlib(layout= "circular", vertex_size= 700, fs= 12, lw= 2, path= "images/fig_3_7.png")
print("DH = {}".format(g.distance_hereditary(print_nodes= True)))
print("DP = {}".format(g.distance_preserving()))

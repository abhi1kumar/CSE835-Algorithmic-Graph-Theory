
import os, sys
sys.path.append(os.getcwd())
from pglib.pg import *

g = petersen_graph()
g.draw_matplotlib(layout= "circular", path= "fig_1.png")

g =  Graph({0: {1: 1, 3: 1}, 1: {0: 1}, 2: {3: 1}, 3: {0: 1, 2: 1}})
g.draw_matplotlib(layout= "circular", path= "fig_2.png")
g.draw_tkz_graph()


import os, sys
sys.path.append(os.getcwd())

import numpy as np
from pg import *
from matplotlib import pyplot as plt

np.random.seed(0)
random.seed(0)

deg_seq = [10,9,8,8,7,7,7,6,6,6,6,5,5,4,4,4,4,4,3,3,3,3,3,3,2,2,2,2,2,1,1,1,1]

g= random_graph_eds01(w= deg_seq)
g.draw_matplotlib(layout= "circular", vertex_size= 700, fs= 12, lw= 2, path= "images/fig_3_10.png", radius_self_loop= 0.25)

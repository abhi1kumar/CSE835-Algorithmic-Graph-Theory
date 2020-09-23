

import os, sys
sys.path.append(os.getcwd())

import numpy as np

from pg import *
import plotting_params as params
from common_operations import *
from matplotlib import pyplot as plt
import matplotlib

radius_self_loop = 0

# Part 1
g =  Graph({0: {1: 1, 2: 1, 4: 1}, 1: {0: 1, 2: 1}, 2: {0: 1, 1: 1, 3: 1}, 3: {2: 1}, 4: {0: 1}})
g.draw_matplotlib(layout= "circular", path= "images/fig_8a.png")

g = g.complement()
g.draw_matplotlib(layout= "circular", path= "images/fig_8a_comp.png", radius_self_loop= radius_self_loop)

# Part 2
g =  Graph({0: {1: 1, 2: 1, 4: 1}, 1: {0: 1, 2: 1}, 2: {0: 1, 1: 1}, 3: {4: 1}, 4: {0: 1, 3: 1}})
g.draw_matplotlib(layout= "circular", path= "images/fig_8b.png")

g = g.complement()
g.draw_matplotlib(layout= "circular", path= "images/fig_8b_comp.png")

# Part 2
g =  Graph({0: {1: 1, 4: 1}, 1: {0: 1, 2: 1}, 2: {1: 1, 3: 1}, 3: {2: 1, 4: 1}, 4: {0: 1, 3: 1}})
g.draw_matplotlib(layout= "circular", path= "images/fig_8c.png")

g = g.complement()
g.draw_matplotlib(layout= "circular", path= "images/fig_8c_comp.png")



import os, sys
sys.path.append(os.getcwd())

import numpy as np

from pg import *
import plotting_params as params
from common_operations import *
from matplotlib import pyplot as plt
import matplotlib

g =  Graph({0: {1: 1}, 1: {0: 1, 3: 1}, 2: {3: 1}, 3: {1: 1, 2: 1}})
g.draw_matplotlib(layout= "circular", path= "images/fig_7a.png", radius_self_loop= 0.25)

g =  Graph({0: {2: 1, 3: 1}, 1: {2: 1}, 2: {0: 1, 1: 1}, 3: {0: 1}})
g.draw_matplotlib(layout= "circular", path= "images/fig_7b.png", radius_self_loop= 0.25)

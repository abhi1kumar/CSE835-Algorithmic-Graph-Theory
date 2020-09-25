

import os, sys
sys.path.append(os.getcwd())

import numpy as np

from pg import *

seq = [4, 4, 3, 3, 2, 2, 2]
result, g_dict = isgraphical(seq)
print(result)
if g_dict is not None:
    g = Graph(g_dict)    
    g.draw_matplotlib(path= "images/fig_12a.png")

seq = [8, 6, 6, 6, 6, 6, 5, 5, 4, 2]
result, g_dict = isgraphical(seq)
print(result)
if g_dict is not None:
    g = Graph(g_dict)
    g.draw_matplotlib(path= "images/fig_12b.png")

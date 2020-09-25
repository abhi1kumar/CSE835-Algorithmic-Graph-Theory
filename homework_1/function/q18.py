
import os, sys
sys.path.append(os.getcwd())

import numpy as np

from pg import *

seq = [1, 1]
result, g_dict = isgraphical(seq)
if g_dict is not None:
    g = Graph(g_dict)    
    g.draw_matplotlib(path= "images/fig_18_n_2.png")

seq = [2, 1, 1]
result, g_dict = isgraphical(seq)
if g_dict is not None:
    g = Graph(g_dict)
    g.draw_matplotlib(path= "images/fig_18_n_3.png")

seq = [3, 2, 2, 1]
result, g_dict = isgraphical(seq)
if g_dict is not None:
    g = Graph(g_dict)
    g.draw_matplotlib(path= "images/fig_18_n_4.png")

seq = [4, 3, 2, 2, 1]
result, g_dict = isgraphical(seq)
if g_dict is not None:
    g = Graph(g_dict)
    g.draw_matplotlib(path= "images/fig_18_n_5.png")

seq = [5, 4, 3, 3, 2, 1]
result, g_dict = isgraphical(seq)
if g_dict is not None:
    g = Graph(g_dict)
    g.draw_matplotlib(path= "images/fig_18_n_6.png")

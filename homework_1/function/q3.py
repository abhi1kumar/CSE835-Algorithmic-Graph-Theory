
import os, sys
sys.path.append(os.getcwd())

import numpy as np

from pg import *
import plotting_params as params
from common_operations import *
from matplotlib import pyplot as plt
import matplotlib

g =  Graph({0: {1: 1}, 1: {0: 1}, 2: {2: 1}})
g.draw_matplotlib(layout= "circular", path= "images/fig_3.png", radius_self_loop= 0.25)

fig = plt.figure(figsize= (10,8), dpi= params.DPI)
matplotlib.rcParams.update({'font.size': 20})
num_points = 101
x = np.arange(1, num_points)

y1 = x - 1
y2 = num_points - 1 - x
ybound = (num_points/2 -1) * np.ones(x.shape)
ymin = np.min(np.vstack((y1[np.newaxis, :], y2[np.newaxis, :])), axis= 0)

plt.plot(x, y1  , lw= params.lw+1, label= r'$x-1$', color= 'orange')
plt.plot(x, y2  , lw= params.lw+1, label= r'$n-x-1$', color= 'dodgerblue')
plt.plot(x, ybound, 'k--', lw= params.lw-1)
plt.plot(x, ymin, lw= params.lw-1, label= r'$\min(x-1, n-x-1)$', color= 'limegreen')

plt.xlabel('x')
plt.xlim(1, num_points-1)
plt.ylim(0, num_points-1)
plt.xticks([1, 0.25*num_points, num_points/2, 0.75*num_points, num_points-1])
plt.yticks([0, 0.25*num_points-1, num_points/2-1, 0.75*num_points-1, num_points-2])
frame1 = plt.gca()
frame1.axes.xaxis.set_ticklabels([r'$1$', '', r'$n/2$', '', r'$n-1$'])
frame1.axes.yaxis.set_ticklabels([r'$0$', '', r'$\frac{n-2}{2}$', '', r'$n-2$'])

plt.grid()
plt.legend(loc= 'upper center')
savefig(plt, "images/fig_3b.png")
plt.show()
plt.close()

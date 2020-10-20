
import os, sys
sys.path.append(os.getcwd())

import numpy as np
from pg import *
from matplotlib import pyplot as plt

np.random.seed(0)
random.seed(0)

n = 40
edge_prob = 0.5
num_iter = 100
edges      = np.zeros((num_iter, ))
degree_seq = np.zeros((num_iter, n))
degrees_binned = np.zeros((num_iter, n))
histogram_bins = np.arange(n+1)
repeated_nodes = 0

for i in range(num_iter):
    g = random_graph(n, edge_prob)
    edges[i]      = g.size()
    degree_seq[i] = np.array(g.degree_sequence())
    degrees_binned_instance = np.histogram(degree_seq[i], histogram_bins)[0]
    degrees_binned[i] = degrees_binned_instance 
    repeated_nodes += np.sum(degrees_binned_instance[degrees_binned_instance > 1])

print("Average number of edges       = ", np.mean(edges))
print("Average degree of vertex      = ", np.mean(degree_seq))
print("No of vertex with same degree = ", repeated_nodes)
print("%  of vertex with same degree = ", repeated_nodes*100.0/(n*num_iter))
degree_seq = degree_seq.flatten()
plt.figure(figsize= params.size, dpi= params.DPI)
plt.hist(degree_seq, bins= histogram_bins, color= "dodgerblue")
plt.grid()
plt.xlim((0, n))
plt.xlabel('degree')
plt.ylabel('frequency')
savefig(plt, "images/fig_3_9.png", tight_flag= True)

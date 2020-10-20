
import os, sys
sys.path.append(os.getcwd())

import numpy as np
from pg import *
from matplotlib import pyplot as plt

np.random.seed(0)
random.seed(0)

n = 40
edge_prob = 0.5
num_iter = 1
edges      = np.zeros((num_iter, ))
degree_seq = np.zeros((num_iter, n))

for i in range(num_iter):
    g = random_graph(n, edge_prob)
    edges[i]      = g.size()
    degree_seq[i] = np.array(g.degree_sequence())

print(np.mean(edges))
print(np.mean(degree_seq))

degree_seq = degree_seq.flatten()
num_bins   = int(np.max(degree_seq))
plt.hist(degree_seq, bins= num_bins)
plt.show()

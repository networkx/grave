"""
Plot a Weighted Adjacency Matrix
---------------------

Basic example of weighted adjacency matrix plotting.

"""

from grave.stats import plot_adjacency_matrix
from grave import plot_network
from networkx.generators.random_graphs import barabasi_albert_graph
import matplotlib.pyplot as plt
import numpy as np

# Generating a networkx graph
network = barabasi_albert_graph(50, 3)

# Give it random edge weights
weights = np.random.normal(loc=10, scale=5, size=network.number_of_edges())
for w, (u, v, attrs) in zip(weights, network.edges.data()):
    attrs['weight'] = w

fig, ax_mat = plt.subplots(figsize=(16, 8), ncols=2)

plot_network(network, ax=ax_mat[0])

plot_adjacency_matrix(network,
                      weighted=True,
                      ax=ax_mat[1])
plt.show()

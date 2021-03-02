"""
Plot an Adjacency Matrix
---------------------

"""

from grave.stats import plot_adjacency_matrix
from networkx.generators.random_graphs import barabasi_albert_graph
import matplotlib.pyplot as plt

# Generating a networkx graph
graph = barabasi_albert_graph(50, 3)

fig, ax_mat = plt.subplots(figsize=(12, 6), ncols=2)
plot_adjacency_matrix(graph, ax=ax_mat[0])
ax_mat[0].set_title('Default Style', x=0.5, y=-0.1)

plot_adjacency_matrix(graph,
                      xticklabels=False,
                      yticklabels=False,
                      linewidths=0,
                      ax=ax_mat[1])
ax_mat[1].set_title('A Minimalist Style', x=0.5, y=-0.1)
plt.show()

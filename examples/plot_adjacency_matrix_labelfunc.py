"""
Plot an Adjacency Matrix with Custom Labels
---------------------

"""

from grave.stats import plot_adjacency_matrix
from networkx.generators.random_graphs import barabasi_albert_graph
import matplotlib.pyplot as plt

# Generating a networkx graph
graph = barabasi_albert_graph(50, 3)

for node, node_attrs in graph.nodes.data():
    node_attrs['label'] = 'Node {0}'.format(str(node))


fig, ax= plt.subplots(figsize=(8, 8))
plot_adjacency_matrix(graph, ax=ax)
plt.show()

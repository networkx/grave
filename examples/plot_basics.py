"""
A dead simple network
---------------------

The simplest way to plot a graphe ever. And yet it looks cool!
"""

import networkx as nx
import matplotlib.pyplot as plt
from grave import plot_network

# Generating a networkx graph
graph = nx.barbell_graph(10, 14)

fig, ax = plt.subplots()
plot_network(graph, ax=ax)
plt.show()

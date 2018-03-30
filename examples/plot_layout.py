"""
Different layouts
=================

GraVE supports different layouts by default.
"""

import networkx as nx
import matplotlib.pyplot as plt
from grave import grave


graph = nx.barbell_graph(10, 14)
nx.set_node_attributes(graph, dict(graph.degree()), 'degree')

fig, axes = plt.subplots(nrows=2, ncols=2)

grave.plot_network(graph, ax=axes[0, 0], layout="spring")
axes[0, 0].set_title("spring", fontweight="bold")

grave.plot_network(graph, ax=axes[1, 0], layout="circular")
axes[1, 0].set_title("circular", fontweight="bold")

grave.plot_network(graph, ax=axes[0, 1], layout="random")
axes[0, 1].set_title("random", fontweight="bold")

grave.plot_network(graph, ax=axes[1, 1], layout="spectral")
axes[1, 1].set_title("spectral", fontweight="bold")

plt.show()

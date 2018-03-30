"""
A simple network
----------------

Test
"""
import networkx as nx
import matplotlib.pyplot as plt
from grave import plot_network


graph = nx.barbell_graph(10, 14)

nx.set_node_attributes(graph, dict(graph.degree()), 'degree')


fig, ax = plt.subplots()
plot_network(graph, ax=ax)
plt.show()

"""
GraVE Documentation
-------------------

"""
import networkx as nx
from networkx.algorithms.approximation.dominating_set import min_weighted_dominating_set
import matplotlib.pyplot as plt

from grave import plot_network, use_attributes

toy_network = nx.barbell_graph(10, 14)
dom_set = min_weighted_dominating_set(toy_network)

for node, node_attrs in toy_network.nodes(data=True):
    if node in dom_set:
        node_attrs['color'] = 'red'
    else:
        node_attrs['color'] = 'black'
    node_attrs['size'] = 50

fig, ax = plt.subplots()
plot_network(toy_network,
             node_style=use_attributes())
plt.show()

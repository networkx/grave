"""
GraVE Documentation
-------------------

Test
"""
import networkx as nx
import matplotlib.pyplot as plt

from grave import grave


graph = nx.barbell_graph(10, 14)
nx.set_node_attributes(graph, dict(graph.degree()), 'degree')


def degree_colorer(node_attributes):
    deg = node_attributes['degree']
    if deg > 5:
        return {'color': 'r', 'size': 10*deg}
    return {'color': 'b', 'size': 10*deg}


fig, ax = plt.subplots()
grave.plot_network(graph, ax=ax, node_style=degree_colorer)
plt.show()

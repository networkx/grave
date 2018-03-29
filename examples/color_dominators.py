"""
GraVE Documentation
-------------------

"""
import networkx as nx
from networkx.algorithms.approximation.dominating_set import min_weighted_dominating_set
import matplotlib.pyplot as plt
from grave import grave

toy_network = nx.barbell_graph(10, 10)

dom_set = min_weighted_dominating_set(toy_network)

for node, node_attrs in toy_network.nodes(data=True):
    node_attrs['is_dominator'] = True if node in dom_set else False


def color_dominators(node_attributes):
    if node_attributes.get('is_dominator'):
        return {'color': 'red'}
    else:
        return {'color': 'gray'}

fig, ax = plt.subplots()
grave.plot_network(toy_network,
                   node_style=color_dominators)
plt.show()

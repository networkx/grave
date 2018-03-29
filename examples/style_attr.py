"""
GraVE Documentation
-------------------

"""

import networkx as nx

toy_network = nx.barbell_graph(100, 10)


for node, node_attributes in toy_network.nodes(data=True):
    node['style'] = {'color': 'blue'}

plot_the_graph(toy_network,
               node_style=lambda attrs: attrs['style'])

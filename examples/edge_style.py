"""
GraVE Documentation
-------------------

"""
import networkx as nx
from grave import grave
from grave.style import use_attributes

toy_network = nx.barbell_graph(10, 14)

node_options = {
    'node_color': 'royalblue',
    'node_size': 50,
    'edgecolors': 'white',
}

edge_options = {
    'line_color': 'grey',
    'alpha': 0.7,
}

for u, v, edge_attributes in toy_network.edges.data():
    c = (toy_network.nodes[u]['value'] +
         toy_network.nodes[v]['value']) / 2
    edge_attributes['color'] = c


def edge_style(edge_attributes):
    return {'linewidth': edge_attributes.get('weight', 1)}



# TODO add spec
WHITELIST = {'color', 'linewidth'}


def get_all_the_styles(attributes):
    return {k: v for k, v in attributes.items()
            if k in WHITELIST}


plot_the_network_as_ball_and_stick(ax, toy_network,
                                   layout='spring',
                                   node_style=get_all_the_styles,
                                   edge_stlye=use_attributes('color'))

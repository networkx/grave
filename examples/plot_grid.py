"""
Labeled 2D Grid
---------------

This example shows both labels and custom layout.
"""
import networkx as nx
import matplotlib.pyplot as plt
import random
from grave import plot_network, style_merger



def degree_colorer(node_attributes):
    deg = node_attributes['degree']
    shape = 'o' #random.choice(['s', 'o', '^', 'v', '8'])
    return {'color': 'b', 'size': 20*deg, 'shape': shape}

def font_styler(attributes):
    return {'font_size': 8,
            'font_weight': .5,
            'font_color': 'k'}

def tiny_font_styler(attributes):
    return {'font_size': 4,
            'font_weight': .5,
            'font_color': 'r'}

def pathological_edge_style(edge_attrs):
    return {'color': random.choice(['r', (0, 1, 0, .5), 'xkcd:ocean'])}


network = nx.grid_2d_graph(4, 6)

nx.set_node_attributes(network, dict(network.degree()), 'degree')

fig, ax = plt.subplots()
plot_network(network, ax=ax, layout=lambda G: {node: node for node in G},
             node_style=degree_colorer,
             edge_style=pathological_edge_style,
             node_label_style=font_styler,
             edge_label_style=tiny_font_styler)

plt.show()

import pytest

import networkx as nx

from grave import plot_network
import matplotlib as mpl
mpl.use('PS', warn=False)

import matplotlib.pyplot as plt
plt.rcParams['text.usetex'] = False


def test_smoke_graph():
    graph = nx.barbell_graph(10, 14)
    plot_network(graph)


def test_graph_no_edges():
    graph = nx.Graph()
    graph.add_node(0)
    plot_network(graph)

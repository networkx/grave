import pytest

import networkx as nx

import matplotlib as mpl
mpl.use('PS', warn=False)
import matplotlib.pyplot as plt
plt.rcParams['text.usetex'] = False

from grave import plot_network


def test_empty_graph():
    G = nx.barbell_graph(10, 14)
    plot_network(G)

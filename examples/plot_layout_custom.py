"""
Using a custom layout
=====================

The default layouts available through GraVE may not be sufficient for ones
need. Hence, GraVE also support custom layouts.


"""
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from grave import grave


graph = nx.barbell_graph(10, 14)
nx.set_node_attributes(graph, dict(graph.degree()), 'degree')


def random_constrained_layout(networkx):
    """
    Let's build my own layout. It's going to be random, except for a handful
    of points!
    """
    n_nodes = len(graph.nodes.data())
    random_state = np.random.RandomState(seed=0)
    xy = random_state.randn(n_nodes, 2)
    xy[0] = [0, 0]
    xy[10] = [+3, 8]

    return {k: xy[k] for k in graph.nodes.keys()}


fig, ax = plt.subplots()
grave.plot_network(graph, ax=ax, layout=random_constrained_layout)

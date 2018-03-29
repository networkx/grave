import matplotlib.pyplot as plt
import networkx as nx
from ._nx_pylab import draw_networkx_nodes, draw_networkx_edges


def plot_network(graph, layout="spring", node_style=None, edge_style=None,
                 axes=None):
    """
    Plot network

    Parameters
    ----------

    graph : networkx graph object
    """
    if axes is None:
        axes = plt.gca()

    pos = nx.spring_layout(graph)
    draw_networkx_nodes(graph, pos)
    draw_networkx_edges(graph, pos)

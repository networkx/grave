import matplotlib.pyplot as plt


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

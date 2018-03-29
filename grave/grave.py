import networkx as nx
from ._nx_pylab import draw_networkx_nodes, draw_networkx_edges
from functools import wraps
import numpy as np
from .style import generate_node_styles

def _ensure_ax(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'ax' not in kwargs:
            import matplotlib.pyplot as plt
            kwargs['ax'] = plt.gca()
        return func(*args, **kwargs)

    return inner


def _generate_node_artist(pos, styles, *, ax):
    N = len(pos)
    proto_node = next(iter(pos))

    x = np.zeros(N) * np.nan
    y = np.zeros(N) * np.nan
    properties = {k: [None] * N for k in styles[proto_node]}

    for j, node in enumerate(pos):
        x[j], y[j] = pos[node]
        for key, values in properties.items():
            values[j] = styles[node][key]

    key_map = {'size': 's', 'color': 'c', 'shape': 'marker',
               'width': 'linewidths', 'edgecolor': 'edgecolors'}
    renamed_properties = {key_map[k]: v
                          for k, v in properties.items()}

    return ax.scatter(x, y, **renamed_properties)


@_ensure_ax
def plot_network(graph, layout="spring", node_style=None, edge_style=None,
                 *, ax):
    """
    Plot network

    Parameters
    ----------

    graph : networkx graph object
    """
    arts = []
    if node_style is None:
        node_style = {}

    pos = nx.spring_layout(graph)
    node_style_dict = generate_node_styles(graph, node_style)
    arts.append(
        _generate_node_artist(pos, node_style_dict, ax=ax))
    # draw_networkx_nodes(graph, pos, ax=ax)
    draw_networkx_edges(graph, pos, ax=ax)

    return arts

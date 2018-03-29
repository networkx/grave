import networkx as nx
from functools import wraps
import numpy as np
from .style import generate_node_styles, generate_edge_styles
from matplotlib.collections import LineCollection


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
    properties = {k: [None] * N for k in styles[proto_node]
                  if k in _VALID_NODE_STYLE}

    for j, node in enumerate(pos):
        x[j], y[j] = pos[node]
        for key, values in properties.items():
            values[j] = styles[node][key]

    key_map = {'size': 's', 'color': 'c', 'shape': 'marker',
               'width': 'linewidths', 'edgecolor': 'edgecolors'}
    renamed_properties = {key_map[k]: v
                          for k, v in properties.items()}

    return ax.scatter(x, y, zorder=2, **renamed_properties)


def _generate_straight_edges(edges, pos, styles, *, ax):
    N = len(edges)
    proto_edge = next(iter(edges))
    edge_pos = [None] * N

    properties = {k: [None] * N for k in styles[proto_edge]
                  if k in _VALID_EDGE_STYLE}

    for j, (u, v) in enumerate(edges):
        edge_pos[j] = (pos[u], pos[v])
        for key, values in properties.items():
            values[j] = styles[(u, v)][key]
    key_map = {'color': 'colors',
               'width': 'linewidths',
               'style': 'linestyle'}

    renamed_properties = {key_map[k]: v
                          for k, v in properties.items()}
    line_art = LineCollection(edge_pos,
                              transOffset=ax.transData,
                              zorder=1,
                              **renamed_properties)
    ax.add_collection(line_art)
    return line_art


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

    if edge_style is None:
        edge_style = {}

    pos = nx.spring_layout(graph)

    # draw_networkx_edges(graph, pos, ax=ax)
    edge_style_dict = generate_edge_styles(graph, edge_style)
    arts.append(
        _generate_straight_edges(graph.edges(), pos,
                                 edge_style_dict, ax=ax))
    node_style_dict = generate_node_styles(graph, node_style)
    arts.append(
        _generate_node_artist(pos, node_style_dict, ax=ax))
    # draw_networkx_nodes(graph, pos, ax=ax)

    return arts

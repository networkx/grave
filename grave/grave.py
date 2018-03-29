import matplotlib.pyplot as plt
import networkx as nx
from ._nx_pylab import draw_networkx_nodes, draw_networkx_edges
from functools import wraps


def _ensure_ax(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'ax' not in kwargs:
            import maptlotlib.pyplot as plt
            kwargs['ax'] = plt.gca()
        return func(*args, **kwargs)

    return inner


def style_merger(*funcs):
    def inner(node_attributes):
        out = {}
        for f in funcs:
            out.update(f(node_attributes))
        return out

    return inner


@_ensure_ax
def plot_network(graph, layout="spring", node_style=None, edge_style=None,
                 *, ax):
    """
    Plot network

    Parameters
    ----------

    graph : networkx graph object
    """
    pos = nx.spring_layout(graph)
    draw_networkx_nodes(graph, pos, ax=ax)
    draw_networkx_edges(graph, pos, ax=ax)

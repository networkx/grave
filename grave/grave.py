import networkx as nx
from functools import wraps
import numpy as np
from .style import (generate_node_styles,
                    generate_edge_styles,
                    _VALID_NODE_STYLE,
                    _VALID_EDGE_STYLE)
from matplotlib.collections import LineCollection, PathCollection
from matplotlib.markers import MarkerStyle
import matplotlib.transforms as mtransforms

from ._layout import _apply_layout
from matplotlib.artist import Artist



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

    key_map = {'size': 'sizes', 'color': 'facecolors', 'shape': 'marker',
               'width': 'linewidths', 'edgecolor': 'edgecolors'}
    renamed_properties = {key_map[k]: v
                          for k, v in properties.items()}

    markers = renamed_properties.pop('marker', None)

    if markers is None:
        paths = (MarkerStyle('o'), )
    else:
        paths = [MarkerStyle(m) for m in markers]
    paths = [p.get_path().transformed(p.get_transform()) for p in paths]

    offsets = np.column_stack([x, y])
    node_art = PathCollection(paths,
                              offsets=offsets,
                              transOffset=ax.transData,
                              **renamed_properties)
    node_art.set_transform(mtransforms.IdentityTransform())

    return node_art,


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
    line_art.set_transform(ax.transData)
    return line_art,


class NXArtist(Artist):
    def __init__(self, graph, layout, node_style, edge_style):
        super().__init__()
        self.graph = graph
        self.layout = layout
        self.node_style = node_style
        self.edge_style = edge_style

        self._children = []

    def get_children(self):
        return list(self._children)

    def _reprocess(self):
        self._children.clear()
        arts = self._children

        graph = self.graph
        edge_style = self.edge_style
        node_style = self.node_style

        pos = _apply_layout(self.layout, graph)

        edge_style_dict = generate_edge_styles(graph, edge_style)
        arts.extend(
            _generate_straight_edges(graph.edges(), pos,
                                     edge_style_dict, ax=self.axes))
        node_style_dict = generate_node_styles(graph, node_style)
        arts.extend(
            _generate_node_artist(pos, node_style_dict, ax=self.axes))

        # TODO sort out all of the things that need to be forwarded
        for child in arts:
            # set the figure / axes on child, this is needed
            # by some internals
            child.set_figure(self.figure)
            child.axes = self.axes
            # forward the clippath/box to the children need this logic
            # because mpl exposes some fast-path logic
            clip_path = self.get_clip_path()
            if clip_path is None:
                clip_box = self.get_clip_box()
                child.set_clip_box(clip_box)
            else:
                child.set_clip_path(clip_path)

    def draw(self, renderer, *args, **kwargs):
        self.stale = False
        if not self._children:
            self._reprocess()

        for art in self._children:
            art.draw(renderer, *args, **kwargs)


@_ensure_ax
def plot_network(graph, layout="spring",
                 node_style=None,
                 edge_style=None,
                 *, ax):
    """
    Plot network

    Parameters
    ----------

    graph : networkx graph object
    """
    if node_style is None:
        node_style = {}

    if edge_style is None:
        edge_style = {}

    art = NXArtist(graph, layout, node_style, edge_style)
    ax.add_artist(art)
    ax.set_axis_off()

    return art

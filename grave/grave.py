import networkx as nx
from functools import wraps, partial
import numpy as np
from .style import (generate_node_styles,
                    generate_edge_styles,
                    _VALID_NODE_STYLE,
                    _VALID_EDGE_STYLE)
from matplotlib.collections import LineCollection, PathCollection
from matplotlib.markers import MarkerStyle
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
    node_indx = [None] * N
    x = np.zeros(N) * np.nan
    y = np.zeros(N) * np.nan
    properties = {k: [None] * N for k in styles[proto_node]
                  if k in _VALID_NODE_STYLE}

    for j, node in enumerate(pos):
        x[j], y[j] = pos[node]
        for key, values in properties.items():
            values[j] = styles[node][key]
        node_indx[j] = node

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

    return node_art, node_indx


def _generate_straight_edges(edges, pos, styles, *, ax):
    N = len(edges)
    proto_edge = next(iter(edges))
    edge_pos = [None] * N
    edge_indx = [None] * N
    properties = {k: [None] * N for k in styles[proto_edge]
                  if k in _VALID_EDGE_STYLE}

    for j, (u, v) in enumerate(edges):
        edge_pos[j] = (pos[u], pos[v])
        for key, values in properties.items():
            values[j] = styles[(u, v)][key]
        edge_indx[j] = (u, v)
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
    return line_art, edge_indx


def _forwarder(forwards, cls=None):
    if cls is None:
        return partial(_forwarder, forwards)

    def make_forward(name):
        def method(self, *args, **kwargs):
            ret = getattr(cls.mro()[1], name)(self, *args, **kwargs)
            for c in self.get_children():
                getattr(c, name)(*args, **kwargs)
            return ret

        return method

    for f in forwards:
        method = make_forward(f)
        method.__name__ = f
        method.__doc__ = 'broadcasts {} to children'.format(f)
        setattr(cls, f, method)

    return cls


def _stale_wrapper(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        try:
            func(self, *args, **kwargs)
        finally:
            self.stale = False
    return inner


@_forwarder(('set_clip_path', 'set_clip_box', 'set_transform',
             'set_snap', 'set_sketch_params', 'set_figure',
             'set_animated'))
class NXArtist(Artist):
    def __init__(self, graph, layout, node_style, edge_style):
        super().__init__()
        self.graph = graph
        self.layout = layout
        self.node_style = node_style
        self.edge_style = edge_style

        # update the layout once so we can use
        # get_datalim before we draw
        self._pos = _apply_layout(self.layout, graph)
        self._node_artist = None
        self._node_indx = None
        self._edge_artist = None
        self._edge_indx = None

    def _clear_state(self):
        self._node_artist = None
        self._node_indx = None
        self._edge_artist = None
        self._edge_indx = None

    def get_children(self):
        return tuple(a for a in (self._node_artist, self._edge_artist)
                     if a is not None)

    def get_datalim(self):
        pos = np.vstack(list(self._pos.values()))

        mins = pos.min(axis=0)
        maxs = pos.max(axis=0)

        return (mins, maxs)

    def _reprocess(self, *, reset_pos=True):
        # nuke old state and mark as stale
        self._clear_state()
        self.stale = True

        # get local refs to everything (just for less typing)
        graph = self.graph
        edge_style = self.edge_style
        node_style = self.node_style

        # update the layout
        if reset_pos:
            self._pos = _apply_layout(self.layout, graph)
        pos = self._pos

        # handle the edges
        edge_style_dict = generate_edge_styles(graph, edge_style)
        self._edge_artist, self._edge_indx = (
            _generate_straight_edges(graph.edges(), pos,
                                     edge_style_dict, ax=self.axes))

        # handle the nodes
        node_style_dict = generate_node_styles(graph, node_style)
        self._node_artist, self._node_indx = (
            _generate_node_artist(pos, node_style_dict, ax=self.axes))

        # TODO handle the text

        # TODO sort out all of the things that need to be forwarded
        for child in self.get_children():
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

    @_stale_wrapper
    def draw(self, renderer, *args, **kwargs):
        if not self.get_visible():
            return

        if not self.get_children():
            self._reprocess()

        for art in self.get_children():
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
    art._reprocess()
    ax.update_datalim(art.get_datalim())
    ax.autoscale_view()
    ax.set_axis_off()

    return art

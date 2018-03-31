import networkx as nx
from functools import wraps, partial
import numpy as np
from matplotlib.collections import LineCollection, PathCollection
from matplotlib.markers import MarkerStyle
from matplotlib.artist import Artist

from ._layout import _apply_layout
from .style import (generate_node_styles,
                    generate_edge_styles,
                    generate_node_label_styles,
                    generate_edge_label_styles,
                    _VALID_NODE_STYLE,
                    _VALID_EDGE_STYLE,
                    _VALID_NODE_LABEL_STYLE,
                    _VALID_EDGE_LABEL_STYLE)


def _ensure_ax(func):
    """Ensure that the wrapped function get an Axes

    If one is not passed in explicitly, ask pyplot for the current Axes
    """
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


def _generate_node_labels(pos, styles, *, ax):
    key_map = {'font_size': 'size',
               'font_color': 'color',
               'font_family': 'family',
               'font_weight': 'weight',
               'alpha': 'alpha',
               'bbox': 'bbox',
               'horizontalalignment': 'horizontalalignment',
               'verticalalignment': 'verticalalignment'}

    node_labels_dict = {}
    for node, nstyle in styles.items():
        properties = {key_map[k]: v for k, v in nstyle.items()
                      if k in key_map}

        x, y = pos[node]

        if 'label' in nstyle:
            label = nstyle['label']
        else:
            label = str(node)    # this makes "1" and 1 the same

        node_labels_dict[node] = ax.text(x, y,
                                         label,
                                         transform=ax.transData,
                                         clip_on=True,
                                         **properties)
    ax.autoscale_view()
    return node_labels_dict


def _generate_edge_labels(pos, styles, *, ax):
    key_map = {'font_size': 'size',
               'font_color': 'color',
               'font_family': 'family',
               'font_weight': 'weight',
               'alpha': 'alpha',
               'bbox': 'bbox',
               'horizontalalignment': 'horizontalalignment',
               'verticalalignment': 'verticalalignment'}

    edge_labels_dict = {}
    for edge, estyle in styles.items():
        properties = {key_map[k]: v for k, v in estyle.items()
                      if k in key_map}

        if 'label' in estyle:
            label = estyle['label']
        else:
            label = str(edge)    # this makes "1" and 1 the same

        if 'label_pos' in estyle:
            label_pos = estyle['label_pos']
        else:
            label_pos = 0.5

        (x1, y1) = pos[edge[0]]
        (x2, y2) = pos[edge[1]]
        (x, y) = (x1 * label_pos + x2 * (1.0 - label_pos),
                  y1 * label_pos + y2 * (1.0 - label_pos))

        if 'rotate' in estyle and estyle['rotate'] is True:
            # in degrees
            angle = np.arctan2(y2 - y1, x2 - x1) / (2.0 * np.pi) * 360
            # make label orientation "right-side-up"
            if angle > 90:
                angle -= 180
            if angle < - 90:
                angle += 180
            # transform data coordinate angle to screen coordinate angle
            xy = np.array((x, y))
            trans_angle = ax.transData.transform_angles(np.array((angle,)),
                                                        xy.reshape((1, 2)))[0]
        else:
            trans_angle = 0.0

        edge_labels_dict[edge] = ax.text(x, y,
                                         label,
                                         rotation=trans_angle,
                                         transform=ax.transData,
                                         clip_on=True,
                                         zorder=1,
                                         **properties)
    ax.autoscale_view()
    return edge_labels_dict


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
             'set_animated', 'set_picker'))
class NXArtist(Artist):
    def __init__(self, graph, layout, node_style, edge_style,
                 node_label_style=None,
                 edge_label_style=None,
                 ):
        super().__init__()
        self.graph = graph
        self.layout = layout
        self.node_style = node_style
        self.edge_style = edge_style
        self.node_label_style = node_label_style
        self.edge_label_style = edge_label_style

        # update the layout once so we can use
        # get_datalim before we draw
        self._pos = _apply_layout(self.layout, graph)
        self._node_artist = None
        self._node_indx = None
        self._edge_artist = None
        self._edge_indx = None
        self._node_label_dict = None
        self._edge_label_dict = None

    def _clear_state(self):
        self._node_artist = None
        self._node_indx = None
        self._edge_artist = None
        self._edge_indx = None
        self._node_label_dict = None
        self._edge_label_dict = None

    def get_children(self):
        artists = [self._edge_artist, self._node_artist]
        if self._node_label_dict is not None:
            artists.extend(self._node_label_dict.values())
        if self._edge_label_dict is not None:
            artists.extend(self._edge_label_dict.values())
        return tuple(a for a in artists if a is not None)

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
        edge_label_style = self.edge_label_style
        node_label_style = self.node_label_style

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

        # handle the node labels
        if node_label_style is not None:
            nlabel_style_dict = generate_node_label_styles(graph,
                                                           node_label_style)
            self._node_label_dict = (
                _generate_node_labels(pos, nlabel_style_dict, ax=self.axes))

        # handle the edge labels
        if edge_label_style is not None:
            elabel_style_dict = generate_edge_label_styles(graph,
                                                           edge_label_style)
            self._edge_label_artist = (
                _generate_edge_labels(pos, elabel_style_dict, ax=self.axes))

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

        elif self.stale:
            self._reprocess(reset_pos=False)

        for art in self.get_children():
            art.draw(renderer, *args, **kwargs)

    def contains(self, mouseevent):
        props = {}
        edge_hit, edge_props = self._edge_artist.contains(mouseevent)
        node_hit, node_props = self._node_artist.contains(mouseevent)
        props['nodes'] = [self._node_indx[j]
                          for j in node_props.get('ind', [])]
        props['edges'] = [self._edge_indx[j]
                          for j in edge_props.get('ind', [])]

        return edge_hit | node_hit, props

    def pick(self, mouseevent):
        # Pick self
        if self.pickable():
            picker = self.get_picker()
            if callable(picker):
                inside, prop = picker(self, mouseevent)
            else:
                inside, prop = self.contains(mouseevent)
            if inside:
                self.figure.canvas.pick_event(mouseevent, self, **prop)


@_ensure_ax
def plot_network(graph, layout="spring",
                 node_style=None,
                 edge_style=None,
                 node_label_style=None,
                 edge_label_style=None,
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

    art = NXArtist(graph, layout, node_style, edge_style,
                   node_label_style, edge_label_style)
    ax.add_artist(art)
    art._reprocess()
    ax.update_datalim(art.get_datalim())
    ax.autoscale_view()
    ax.set_axis_off()

    return art

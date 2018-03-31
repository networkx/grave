
_VALID_NODE_STYLE = ['size', 'color', 'shape', 'width',
                     'edgecolor']

_VALID_EDGE_STYLE = ['color', 'width', 'style']

_VALID_NODE_LABEL_STYLE = ['bbox',
                           'font_size',
                           'font_color',
                           'font_family',
                           'font_weight',
                           'horizontalalignment',
                           'verticalalignment']

_VALID_EDGE_LABEL_STYLE = ['bbox',
                           'label_pos',
                           'rotate',
                           'font_size',
                           'font_color',
                           'font_family',
                           'font_weight',
                           'horizontalalignment',
                           'verticalalignment']

_ALL_STYLE_KEYS = _VALID_NODE_STYLE + _VALID_NODE_LABEL_STYLE + \
                  _VALID_EDGE_STYLE + _VALID_EDGE_LABEL_STYLE


def default_node_style():
    return {'color': 'C0',
            'size': 50,
            'shape': 'o',
            'width': 1,
            'edgecolor': 'white'}


def default_edge_style():
    return {'color': '#292929',
            'width': 1,
            'style': '-'}


# box of white with white border
_BBOX_DEFAULT = dict(boxstyle='round',
                     ec=(1.0, 1.0, 1.0),
                     fc=(1.0, 1.0, 1.0),
                     )


def default_node_label_style():
    return {'bbox': _BBOX_DEFAULT,
            'font_size': 4,
            'font_color': '#292929',
            'font_family': None,
            'font_weight': 1,
            'horizontalalignment': 'center',
            'verticalalignment': 'center'}


def default_edge_label_style():
    return {'bbox': _BBOX_DEFAULT,
            'label_pos': 0.5,
            'rotate': 0,
            'font_size': 4,
            'font_color': '#292929',
            'font_family': None,
            'font_weight': 1,
            'horizontalalignment': 'center',
            'verticalalignment': 'center'}


def default_style():
    return {'node_style': default_node_style,
            'edge_style': default_edge_style}


def style_merger(*funcs):
    def inner(node_attributes):
        out = {}
        for f in funcs:
            out.update(f(node_attributes))
        return out

    return inner


def use_attributes(keys=None):
    '''Utility style function that searches the given
    attribute dictionary for valid style attributes and bundles
    them into a style dictionary.

    Parameters
    ----------
    keys : str or iterable, optional
        Style keys to search for.

    Returns
    -------
    inner : function
        A style function.
    '''

    def inner(attributes):
        if keys is None:
            return {k: attributes[k] for k in _ALL_STYLE_KEYS
                    if k in attributes}
        if isinstance(keys, str):
            return {keys: attributes[keys]} if keys in attributes else {}
        else:
            return {key: attributes[key] for key in keys
                    if key in attributes}
    return inner


def apply_style(style, item_iterable, default):
    styles = {}
    if callable(style):
        for item, item_attr in item_iterable:
            base = default()
            base.update(style(item_attr))
            styles[item] = base
    elif isinstance(style, dict):
        base = default()
        base.update(style)
        for item, item_attr in item_iterable:
            styles[item] = base
    else:
        raise TypeError("style must be dict or callable,"
                        " got {0}".format(type(style)))
    return styles


def generate_node_styles(network, node_style):
    # dict of node id -> node_style_dict
    return apply_style(node_style,
                       network.nodes.items(),
                       default_node_style)


def generate_edge_styles(network, edge_style):
    # dict of edge tuple -> edge_style_dict
    return apply_style(edge_style,
                       network.edges.items(),
                       default_edge_style)


def generate_node_label_styles(network, label_style):
    # returns dict of node id -> node_style_dict
    return apply_style(label_style,
                       network.nodes.items(),
                       default_node_label_style)


def generate_edge_label_styles(network, label_style):
    # returns dict of edge tuple -> edge_style_dict
    return apply_style(label_style,
                       network.edges.items(),
                       default_edge_label_style)

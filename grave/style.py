

def apply_style(style, item_iterable):
    styles = {}
    if callable(style):
        for item, item_attr in item_iterable:
            styles[item] = style(item_attr)
    elif isinstance(style, dict):
        for item, item_attr in item_iterable:
            styles[item] = style
    else:
        raise TypeError("style must be dict or callable,"
                        " got {0}".format(type(style)))
    return styles


def generate_node_styles(network, node_style):
    # dict of node id -> node_style_dict
    return apply_style(node_style, network.nodes.data())


def generate_edge_styles(network, edge_style):
    # dict of edge tuple -> edge_style_dict
    return apply_style(edge_style, network.edges.data())

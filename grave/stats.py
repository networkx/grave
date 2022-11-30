import warnings
import functools

import networkx as nx
import numpy as np
import matplotlib.cm as cm
import matplotlib.colors as mcolors

from .grave import _ensure_ax


def _optional_dependency(dependency):
    def _optional_dependency(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ImportError as e:
                if e.name == dependency:
                    warnings.warn('Optional dependency {0} not installed, '
                                  'returning None!'.format(dependency))
                    return None
                else:
                    raise e
        return wrapper
    return _optional_dependency


@_optional_dependency('seaborn')
@_ensure_ax
def plot_adjacency_matrix(network,
                          node_labels=None,
                          label_behavior=None,
                          weighted=False,
                          frame=True,
                          xtickrotation=70,
                          ytickrotation=0,
                          *, ax,
                          **heatmap_kwargs):
    '''Plot the adjacency matrix of a network. If weight is True, 
    use a `weight` attribute from the edges to plot a heatmap of weights.

    Requires seaborn to be installed.
    Extra keyword parameters are passed on to seaborn's `heatmap` function.

    Parameters
    ----------

    network : networkx graph object
    node_labels : callable, "auto", int, or iterable, optional
        If callable, should be a function taking a node attribute dict
        and returning a string. If None, checks each node for a label
        attribute and uses it if found, or uses str(node).
    weighted : bool, optional
        If True, draw a weighted adjacency matrix using a `weight`
        edge attribute.
    frame : bool, optional
        If True, draw a wider frame around the matrix.
    xtickrotation : int, optional
        Rotation to apply to x axis labels.
    ytickrotation : int, optional
        Rotation to apply to y axis labels.
 
    Returns
    -------
    The matplotlib axes.
    '''
    from seaborn import heatmap
    import pandas as pd
    import matplotlib.pyplot as plt
    import warnings

    params = {'vmin': None,
              'vmax': None,
              'cmap': None,
              'center': None,
              'robust': False,
              'annot': None,
              'fmt': '.2g',
              'annot_kws': None,
              'linecolor': 'lightgray',
              'linewidths': .5,
              'cbar': False,
              'cbar_kws': {'shrink': .5},
              'cbar_ax': None,
              'xticklabels': 'auto',
              'yticklabels': 'auto',
              'square': True,
              'mask': None}
    
    if weighted:
        adj_mat = np.empty((network.number_of_nodes(),
                            network.number_of_nodes()))
        adj_mat[:] = np.NaN

        missing_weight = 0
        directed = nx.is_directed(network)
        node_idx = {node : idx for idx, node in \
                    enumerate(network.nodes.keys())}
        for u, v, edge_attrs in network.edges.data():
            u_idx = node_idx[u]
            v_idx = node_idx[v]
            try:
                weight = edge_attrs['weight']
            except KeyError:
                weight = 0
                missing_weight += 1
            adj_mat[u_idx, v_idx] = weight
            if not directed:
                adj_mat[v_idx, u_idx] = weight

        params['cbar'] = True
        params['cmap'] = plt.get_cmap()

        if missing_weight > 0:
            n_edges = network.number_of_edges()
            warnings.warn('{missing} of {n_edges}'
                          ' edges missing weight attr,'
                          ' using 0 for them.'.format(missing=missing_weight,
                                                      n_edges=n_edges))
    else:
        adj_mat = nx.adj_matrix(network).todense()
        cmap = plt.get_cmap('binary')
        params['cmap'] = cmap

    labels = []
    if callable(node_labels):
        for item, item_attr in network.nodes.data():
            attrs = dict(item_attr)
            labels.append(node_labels(item_attr))
    else:
        for node, node_attr in network.nodes.data():
            labels.append(node_attr.get('label', str(node)))
    
    data = pd.DataFrame(adj_mat, columns=labels, index=labels)
    
    params.update(heatmap_kwargs)
    ax = heatmap(data, ax=ax, **params)

    if frame:
        for axis in ['top','bottom','left','right']:
            ax.spines[axis].set_visible(True)
            ax.spines[axis].set_color(params['linecolor'])
            ax.spines[axis].set_linewidth(2 * params['linewidths'])

    ax.xaxis.tick_top()
    for tick in ax.get_xticklabels():
        tick.set_rotation(xtickrotation)
    for tick in ax.get_yticklabels():
        tick.set_rotation(ytickrotation)

    return ax, data

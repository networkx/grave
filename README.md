# grave

[![Build Status](https://travis-ci.org/networkx/grave.svg?branch=master)](https://travis-ci.org/networkx/grave)

GraVE is a Graph Visualization Package combining ideas from
Matplotlib, NetworkX, and seaborn. Its goal is to provide a
network drawing API that covers the most use cases with sensible
defaults and simple style configuration. Currently, it supports
drawing graphs from NetworkX.

## Example Usage

```python
import network as nx
from networkx.algorithms.approximation.dominating_set import min_weighted_dominating_set

from grave import plot_network

network = nx.barbell_graph(10, 10)
dom_set = min_weighted_dominating_set(network)

for node, node_attrs in network.nodes(data=True):
    node_attrs['is_dominator'] = True if node in dom_set else False

def color_dominator_nodes(node_attrs):
    if node_attrs.get('is_dominator', False):
        return {'color': 'red'}
    else:
        return {'color': 'gray'}

fig, ax = plt.subplots()
plot_network(network, node_style=color_dominators)
plt.show()

```

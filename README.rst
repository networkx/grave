Grave—dead simple graph visualization
=====================================

.. image:: https://travis-ci.org/networkx/grave.svg?branch=main
   :target: https://travis-ci.org/networkx/grave
   :alt: Automated test status (Linux and MacOS)

.. image:: https://ci.appveyor.com/api/projects/status/github/networkx/grave?branch=main&svg=true
   :target: https://ci.appveyor.com/project/networkx/grave
   :alt: Automated test status (Windows)

.. image:: https://codecov.io/gh/networkx/grave/branch/main/graph/badge.svg
  :target: https://codecov.io/gh/networkx/grave
  :alt: Test coverage

.. GH breaks rendering of SVG from the repo, so we redirect through rawgit.com.
   GH ignores the width and align directives for PNGs.

.. image:: https://rawgit.com/networkx/grave/main/doc/_static/default.svg
   :width: 250px
   :align: right
   :alt: Logo

Grave is a graph visualization package combining ideas from Matplotlib,
NetworkX, and seaborn. Its goal is to provide a network drawing API that
covers the most use cases with sensible defaults and simple style
configuration. Currently, it supports drawing graphs from NetworkX.

- **Website (including documentation):** https://networkx.github.io/grave/
- **Mailing list:** https://groups.google.com/forum/#!forum/networkx-discuss
- **Source:** https://github.com/networkx/grave
- **Bug reports:** https://github.com/networkx/grave/issues

Example
-------

Here, we create a graph and color the nodes in its minimum weighted
dominating set:

.. code:: python

    import matplotlib.pyplot as plt
    import networkx as nx
    from networkx.algorithms.approximation.dominating_set import min_weighted_dominating_set

    from grave import plot_network

    network = nx.powerlaw_cluster_graph(50, 1, .2)
    dom_set = min_weighted_dominating_set(network)

    for node, node_attrs in network.nodes(data=True):
        node_attrs['is_dominator'] = True if node in dom_set else False

    def color_dominators(node_attrs):
        if node_attrs.get('is_dominator', False):
            return {'color': 'red'}
        else:
            return {'color': 'black'}

    fig, ax = plt.subplots()
    plot_network(network, node_style=color_dominators)
    plt.show()

The result:

.. image:: https://rawgit.com/networkx/grave/main/doc/_static/dominators.svg
    :width: 700
    :align: center
    :alt: Coloring the minimum weighted dominating set of a graph

License
-------

Released under the 3-Clause BSD license (see `LICENSE`).

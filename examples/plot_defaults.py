"""
Test
====

Test
"""

import networkx as nx
import matplotlib.pyplot as plt
from grave import plot_network

network = nx.binomial_graph(50, .05)

fig, ax_mat = plt.subplots(ncols=2)

plot_network(network, ax=ax_mat[0])
ax_mat[0].set_axis_on()
with plt.style.context(('ggplot')):
    plot_network(network, ax=ax_mat[1])
ax_mat[1].set_axis_on()
for ax in ax_mat:
    ax.set_axis_on()
    ax.tick_params(which='both',
                bottom=False,
                top=False,
                left=False,
                right=False,
                labelbottom=False,
                labelleft=False)
plt.show()

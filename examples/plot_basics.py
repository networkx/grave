import networkx as nx
import matplotlib.pyplot as plt

from grave import grave


graph = nx.barbell_graph(10, 14)

fig, ax = plt.subplots()
grave.plot_network(graph, axes=ax)

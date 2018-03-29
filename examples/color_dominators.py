import networkx as nx

toy_network = nx.barbell_graph(100, 10)

dom_set = nx.min_weight_dominating_set(toy_network)

for node, node_attributes in toy_network.nodes(data=True):
    node['is_dominator'] = True if node in dom_set else False


def color_dominators(node_attributes):
    if node_attributes.get('is_dominator'):
        return {'color': 'red'}
    else:
        return {'color': 'gray'}


plot_the_graph(toy_network,
               node_style=color_dominators)

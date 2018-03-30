import networkx as nx


known_layouts = {
    "spring": nx.spring_layout,
    "circular": nx.circular_layout,
    "random": nx.random_layout,
    "kamada_kawai": nx.kamada_kawai_layout,
    "shell": nx.shell_layout,
    "spectral": nx.spectral_layout,
    }


def _apply_layout(layout, graph):
    if callable(layout):
        return layout(graph)
    elif isinstance(layout, str):
        return known_layouts[layout](graph)
    else:
        raise ValueError("Dunno what do do with this")

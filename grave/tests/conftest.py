import pytest
import networkx as nx


@pytest.fixture
def barbell_network():
    return nx.barbell_graph(10, 10)

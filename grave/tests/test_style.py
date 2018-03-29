import pytest


def test_generate_node_styles_callable(barbell_network):
    from grave.style import apply_style, generate_node_styles
    
    def style_func(attrs):
        return {'color': 'red'}

    node_styles = generate_node_styles(barbell_network,
                                       style_func)
    
    for node, style in node_styles.items():
        assert node in barbell_network
        assert style == {'color': 'red'}


def test_generate_node_styles_dict(barbell_network):
    from grave.style import apply_style, generate_node_styles

    style = {'color': 'red'}

    node_styles = generate_node_styles(barbell_network,
                                       style)

    for node, style in node_styles.items():
        assert node in barbell_network
        assert style == {'color': 'red'}


def test_generate_node_style_typerror(barbell_network):
    from grave.style import apply_style, generate_node_styles

    with pytest.raises(TypeError):
        node_styles = generate_node_styles(barbell_network,
                                       'red')


def test_generate_edge_styles_callable(barbell_network):
    from grave.style import apply_style, generate_edge_styles
    
    def style_func(attrs):
        return {'color': 'red'}

    edge_styles = generate_edge_styles(barbell_network,
                                       style_func)
    
    for edge, style in edge_styles.items():
        assert edge in barbell_network.edges
        assert style == {'color': 'red'}


def test_generate_edge_styles_dict(barbell_network):
    from grave.style import apply_style, generate_edge_styles

    style = {'color': 'red'}

    edge_styles = generate_edge_styles(barbell_network,
                                       style)

    for edge, style in edge_styles.items():
        assert edge in barbell_network.edges
        assert style == {'color': 'red'}


def test_generate_edge_style_typerror(barbell_network):
    from grave.style import apply_style, generate_edge_styles

    with pytest.raises(TypeError):
        edge_styles = generate_edge_styles(barbell_network,
                                       'red')



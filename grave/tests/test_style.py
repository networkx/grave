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

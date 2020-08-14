import pytest

import tools.utils 


def test_cartesian_product():
    # given:
    x = [[1, 2, 3], [4, 5, 6], [1]]

    # when:
    result =  tools.utils.cartesian_product(x)

    # then:
    assert len(result) ==  9
    assert result[:, 2].max() == 1


def test__lazy_cartesian_product():
    # given:
    x = [[1, 2, 3], [4, 5, 6], [1]]

    # when:
    result =  list(tools.utils._lazy_cartesian_product(x))

    # then:
    assert len(result) ==  9


def test_lazy_cartesian_product():
    # given:
    x = [[1, 2, 3], [4, 5, 6], [1]]

    # when:
    result =  list(tools.utils.lazy_cartesian_product(x, 2))

    # then:
    assert len(result) ==  5

@pytest.mark.parametrize("value, expected", [(True, True), ("True", True), ("f", False)])
def test_str2bool(value, expected):
    assert tools.utils.str2bool(value) == expected

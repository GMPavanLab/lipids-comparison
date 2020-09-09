import numpy as np

from tools.metrics import JS 


def test_JS():
    # given:
    p = np.random.randint(0, 1000, size=10) / 1000     
    q = np.random.randint(0, 1000, size=10) / 1000     

    # when:
    result =  JS(p, q)

    # then:
    assert isinstance(result, float)
    assert result >= 0

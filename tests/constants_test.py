import pytest
from gswp import constants

def test_frozen():

    with pytest.raises(TypeError):
        constants.PROBSEVERE[0] = 1

    with pytest.raises(TypeError):
        constants.GMGSI[0] = 1
        
    with pytest.raises(AttributeError):
        constants.PROBSEVERE.PARAMETERS = 1

    with pytest.raises(AttributeError):
        constants.GMGSI.PARAMETERS = 1
        
    with pytest.raises(AttributeError):
        constants.ATMOSPHERE.ABSOLUTE_ZERO = 1
import pytest
from app.operations import Operations

def test_power():
    assert Operations.power(2, 3) == 8

def test_root():
    assert round(Operations.root(27, 3), 5) == 3.0

def test_root_zero_division():
    with pytest.raises(ZeroDivisionError):
        Operations.root(8, 0)

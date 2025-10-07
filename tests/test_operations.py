import pytest

from app.operations import Operations


def test_add():
    assert Operations.add(1, 2) == 3


def test_subtract():
    assert Operations.subtract(5, 3) == 2


def test_multiply():
    assert Operations.multiply(3, 4) == 12


def test_divide():
    assert Operations.divide(10, 2) == 5


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        Operations.divide(1, 0)

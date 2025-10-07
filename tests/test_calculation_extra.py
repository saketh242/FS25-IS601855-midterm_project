import pytest
from app.calculation import CalculationFactory, AddCalculation, SubtractCalculation, MultiplyCalculation, DivideCalculation, PowerCalculation, RootCalculation

def test_factory_power():
    c = CalculationFactory.register_calculation("power", 2, 3)
    assert isinstance(c, PowerCalculation)
    assert c.execute() == 8
    assert str(c) == "2 ^ 3 = 8"

def test_factory_root():
    c = CalculationFactory.register_calculation("root", 27, 3)
    assert isinstance(c, RootCalculation)
    assert round(c.execute(), 5) == 3.0
    assert "root" in str(c)

def test_factory_invalid():
    # Should return None for invalid operation
    assert CalculationFactory.register_calculation("invalid", 1, 2) is None

def test_divide_by_zero_in_calculation():
    c = CalculationFactory.register_calculation("divide", 1, 0)
    with pytest.raises(ZeroDivisionError):
        c.execute()

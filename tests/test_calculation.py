import pytest

from app.calculation import (
    AddCalculation,
    SubtractCalculation,
    MultiplyCalculation,
    DivideCalculation,
    CalculationFactory,
)


def test_add_calculation_execute_and_str():
    c = AddCalculation(2, 3)
    assert c.execute() == 5
    assert str(c) == f"{c.a} + {c.b} = {c.execute()}"


def test_subtract_calculation_execute_and_str():
    c = SubtractCalculation(5, 2)
    assert c.execute() == 3
    assert str(c) == f"{c.a} - {c.b} = {c.execute()}"


def test_multiply_calculation_execute_and_str():
    c = MultiplyCalculation(3, 4)
    assert c.execute() == 12
    assert str(c) == f"{c.a} * {c.b} = {c.execute()}"


def test_divide_calculation_execute_and_str():
    c = DivideCalculation(10, 2)
    assert c.execute() == 5
    assert str(c) == f"{c.a} / {c.b} = {c.execute()}"


def test_factory_register_add():
    c = CalculationFactory.register_calculation("add", 1, 2)
    assert isinstance(c, AddCalculation)


def test_factory_register_subtract():
    c = CalculationFactory.register_calculation("subtract", 5, 3)
    assert isinstance(c, SubtractCalculation)


def test_factory_register_multiply():
    c = CalculationFactory.register_calculation("mulitply", 2, 4)
    assert isinstance(c, MultiplyCalculation)


def test_factory_register_divide():
    c = CalculationFactory.register_calculation("divide", 8, 2)
    assert isinstance(c, DivideCalculation)


def test_call_base_abstract_methods_directly():
    # execute the base Calculation methods (they are no-ops) to cover the 'pass' lines
    from app.calculation import Calculation

    class Dummy:
        pass

    dummy = Dummy()
    # calling the base implementations should simply return None / not raise
    assert Calculation.execute(dummy) is None
    assert Calculation.__str__(dummy) is None


def test_base_init_via_concrete_subclass():
    # create a concrete subclass that doesn't override __init__ so Calculation.__init__ runs
    from app.calculation import Calculation

    class ConcreteCalc(Calculation):
        def execute(self):
            return self.a + self.b

        def __str__(self):
            return f"{self.a}+{self.b}"

    c = ConcreteCalc(7, 8)
    assert c.a == 7
    assert c.b == 8
    assert c.execute() == 15

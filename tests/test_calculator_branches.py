import importlib

from app import calculator as calc_module
from app.calculation import CalculationFactory
from app import calculation as calc_mod
from app.operations import Operations


def test_main_import_does_not_run_calculator():
    # importing main should not start the REPL (calculator is only called under __main__)
    main = importlib.import_module('main')
    assert hasattr(main, 'calculator')


def test_factory_unknown_returns_none():
    c = CalculationFactory.register_calculation('unknown', 1, 2)
    assert c is None


def test_calculator_invalid_input(monkeypatch, capsys):
    inputs = iter(['foo bar', 'exit'])
    monkeypatch.setattr('builtins.input', lambda prompt='': next(inputs))
    calc_module.calculator()
    captured = capsys.readouterr()
    assert 'Invalid input. Please enter an operation followed by two numbers.' in captured.out


def test_calculator_non_numeric(monkeypatch, capsys):
    inputs = iter(['add a b', 'exit'])
    monkeypatch.setattr('builtins.input', lambda prompt='': next(inputs))
    calc_module.calculator()
    captured = capsys.readouterr()
    assert 'Enter not a valid number' in captured.out


def test_calculator_perform_add(monkeypatch, capsys):
    inputs = iter(['add 2 3', 'exit'])
    monkeypatch.setattr('builtins.input', lambda prompt='': next(inputs))
    calc_module.calculator()
    captured = capsys.readouterr()
    assert 'The result is' in captured.out
    assert '5.0' in captured.out


def test_calculator_unexpected_exception(monkeypatch, capsys):
    # Cause register_calculation to raise so generic exception branch executes
    monkeypatch.setattr(CalculationFactory, 'register_calculation', lambda *a, **k: (_ for _ in ()).throw(Exception('boom')))
    inputs = iter(['add 1 2', 'exit'])
    monkeypatch.setattr('builtins.input', lambda prompt='': next(inputs))
    calc_module.calculator()
    captured = capsys.readouterr()
    assert 'Unexpected error' in captured.out


def test_calculator_help_and_history(monkeypatch, capsys):
    # exercise 'help' and then 'history' branches in the REPL
    inputs = iter(['help', 'history', 'exit'])
    monkeypatch.setattr('builtins.input', lambda prompt='': next(inputs))
    calc_module.calculator()
    captured = capsys.readouterr()
    assert 'Type history for history' in captured.out
    assert 'Calculator history' in captured.out


def test_calculator_zero_division_branch(monkeypatch, capsys):
    # Force Operations.divide to raise ZeroDivisionError to hit that except branch
    monkeypatch.setattr(Operations, 'divide', lambda a, b: (_ for _ in ()).throw(ZeroDivisionError('div by zero')))
    inputs = iter(['divide 1 0', 'exit'])
    monkeypatch.setattr('builtins.input', lambda prompt='': next(inputs))
    calc_module.calculator()
    captured = capsys.readouterr()
    assert 'You know we cannot divide by zero' in captured.out

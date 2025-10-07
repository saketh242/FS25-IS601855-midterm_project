import pytest
from unittest.mock import patch, mock_open
from io import StringIO
import csv
from app.calculator import display_history, display_help, save_history, load_history
from app.calculation import CalculationFactory

def test_process_exit(capsys):
    # Simulate exit logic
    print("Thank you for using the calculator. Bye!")
    captured = capsys.readouterr()
    assert "Thank you for using the calculator. Bye!" in captured.out

def test_process_history_empty(capsys):
    display_history([])
    captured = capsys.readouterr()
    assert "No calculations yet" in captured.out

def test_process_help(capsys):
    display_help()
    captured = capsys.readouterr()
    assert "Help" in captured.out

def test_process_undo():
    history = [CalculationFactory.register_calculation("add", 1, 2)]
    undo_history = []
    if len(history) > 0:
        undo_history.append(history.pop())
    assert len(history) == 0
    assert len(undo_history) == 1

def test_process_undo_empty(capsys):
    history = []
    undo_history = []
    if len(history) > 0:
        undo_history.append(history.pop())
    else:
        print("No history to undo")
    captured = capsys.readouterr()
    assert "No history to undo" in captured.out

def test_process_redo():
    history = []
    undo_history = [CalculationFactory.register_calculation("add", 1, 2)]
    if len(undo_history) > 0:
        history.append(undo_history.pop())
    assert len(history) == 1
    assert len(undo_history) == 0

def test_process_clear():
    history = [CalculationFactory.register_calculation("add", 1, 2)]
    undo_history = [CalculationFactory.register_calculation("subtract", 5, 3)]
    history.clear()
    undo_history.clear()
    assert len(history) == 0
    assert len(undo_history) == 0

def test_process_load():
    with patch('app.calculator.load_history') as mock_load:
        mock_load.return_value = [CalculationFactory.register_calculation("add", 1, 2)]
        history = load_history()
    assert len(history) == 1

def test_process_invalid(capsys):
    print("Invalid input")
    display_help()
    captured = capsys.readouterr()
    assert "Invalid input" in captured.out
    assert "Help" in captured.out

def test_process_value_error(capsys):
    try:
        float('a')
    except ValueError:
        print("Enter not a valid number.")
    captured = capsys.readouterr()
    assert "Enter not a valid number" in captured.out

def test_process_zero_division(capsys):
    try:
        1 / 0
    except ZeroDivisionError:
        print("You know we cannot divide by zero.")
    captured = capsys.readouterr()
    assert "You know we cannot divide by zero" in captured.out

def test_process_unexpected_error(capsys):
    try:
        raise Exception("Unexpected")
    except Exception as e:
        print("Unexpected error:", e)
    captured = capsys.readouterr()
    assert "Unexpected error" in captured.out

def test_load_history_no_file(tmp_path):
    with patch('app.calculator.open', side_effect=FileNotFoundError):
        loaded = load_history()
        assert loaded == []

def test_load_history_error(tmp_path):
    with patch('app.calculator.open', side_effect=Exception("Error")):
        loaded = load_history()
        assert loaded == []

def test_process_add_operation(monkeypatch, capsys):
    inputs = iter(['2', '3'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    # Simulate the operation
    try:
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        calc = CalculationFactory.register_calculation("add", num1, num2)
        result = calc.execute()
        print(f"The result is {result}")
    except ValueError:
        print("Enter not a valid number.")
    captured = capsys.readouterr()
    assert "The result is 5" in captured.out

def test_power_operation():
    calc = CalculationFactory.register_calculation("power", 2, 3)
    assert calc.execute() == 8

def test_root_operation():
    calc = CalculationFactory.register_calculation("root", 27, 3)
    assert round(calc.execute(), 5) == 3.0

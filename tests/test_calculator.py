import pytest
from unittest.mock import patch, mock_open
from io import StringIO
import csv
from app.calculator import calculator, display_history, display_help, save_history, load_history
from app.calculation import CalculationFactory

@pytest.fixture
def mock_input():
    return patch('builtins.input')

@pytest.fixture
def mock_print(capsys):
    return capsys

def test_calculator_exit(mock_input):
    mock_input.side_effect = ['exit']
    with pytest.raises(SystemExit) as excinfo:
        calculator()
    assert excinfo.type == SystemExit

def test_calculator_add_operation(mock_input, capsys):
    mock_input.side_effect = ['add', '2', '3', 'exit']
    with patch('app.calculator.log_operation') as mock_log:
        calculator()
    captured = capsys.readouterr()
    assert "The result is 5" in captured.out
    mock_log.assert_called()

def test_calculator_subtract_operation(mock_input, capsys):
    mock_input.side_effect = ['subtract', '5', '3', 'exit']
    calculator()
    captured = capsys.readouterr()
    assert "The result is 2" in captured.out

def test_calculator_multiply_operation(mock_input, capsys):
    mock_input.side_effect = ['multiply', '4', '3', 'exit']
    calculator()
    captured = capsys.readouterr()
    assert "The result is 12" in captured.out

def test_calculator_divide_operation(mock_input, capsys):
    mock_input.side_effect = ['divide', '10', '2', 'exit']
    calculator()
    captured = capsys.readouterr()
    assert "The result is 5" in captured.out

def test_calculator_history(mock_input, capsys):
    mock_input.side_effect = ['add', '1', '2', 'history', 'exit']
    calculator()
    captured = capsys.readouterr()
    assert "1 + 2 = 3" in captured.out

def test_calculator_help(mock_input, capsys):
    mock_input.side_effect = ['help', 'exit']
    calculator()
    captured = capsys.readouterr()
    assert "Help" in captured.out

def test_calculator_undo(mock_input, capsys):
    mock_input.side_effect = ['add', '1', '2', 'undo', 'history', 'exit']
    calculator()
    captured = capsys.readouterr()
    assert "No calculations yet" in captured.out

def test_calculator_redo(mock_input, capsys):
    mock_input.side_effect = ['add', '1', '2', 'undo', 'redo', 'history', 'exit']
    calculator()
    captured = capsys.readouterr()
    assert "1 + 2 = 3" in captured.out

def test_calculator_clear(mock_input, capsys):
    mock_input.side_effect = ['add', '1', '2', 'clear', 'history', 'exit']
    calculator()
    captured = capsys.readouterr()
    assert "No calculations yet" in captured.out

def test_calculator_save_and_load(mock_input, tmp_path):
    csv_path = tmp_path / "calculator.csv"
    with patch('app.calculator.open', mock_open()) as m_open:
        m_open.return_value.__enter__.return_value = StringIO()
        mock_input.side_effect = ['add', '1', '2', 'save', 'exit']
        calculator()
    # Simulate load
    loaded = load_history()
    assert len(loaded) > 0

def test_calculator_invalid_input(mock_input, capsys):
    mock_input.side_effect = ['invalid', 'exit']
    calculator()
    captured = capsys.readouterr()
    assert "Invalid input" in captured.out

def test_calculator_value_error(mock_input, capsys):
    mock_input.side_effect = ['add', 'a', 'exit']
    calculator()
    captured = capsys.readouterr()
    assert "Enter not a valid number" in captured.out

def test_calculator_zero_division(mock_input, capsys):
    mock_input.side_effect = ['divide', '1', '0', 'exit']
    calculator()
    captured = capsys.readouterr()
    assert "You know we cannot divide by zero" in captured.out

def test_calculator_unexpected_error(mock_input, capsys):
    with patch('app.calculation.CalculationFactory.register_calculation') as mock_calc:
        mock_calc.side_effect = Exception("Unexpected")
        mock_input.side_effect = ['add', '1', '2', 'exit']
        calculator()
    captured = capsys.readouterr()
    assert "Unexpected error" in captured.out

def test_save_history(tmp_path):
    calc = CalculationFactory.register_calculation("add", 1, 2)
    csv_path = tmp_path / "calculator.csv"
    with patch('app.calculator.open') as m_open:
        m_open.return_value.__enter__.return_value = csv.writer(StringIO())
        save_history([calc])
    # Assert writer called appropriately

def test_load_history_no_file(tmp_path):
    with patch('app.calculator.open', side_effect=FileNotFoundError):
        loaded = load_history()
        assert loaded == []

def test_load_history_error(tmp_path):
    with patch('app.calculator.open', side_effect=Exception("Error")):
        loaded = load_history()
        assert loaded == []

def test_calculator_undo_empty(mock_input, capsys):
    mock_input.side_effect = ['undo', 'exit']
    calculator()
    captured = capsys.readouterr()
    assert "No history to undo" in captured.out

def test_calculator_redo_empty(mock_input, capsys):
    mock_input.side_effect = ['redo', 'exit']
    calculator()
    captured = capsys.readouterr()
    assert "No history to redo" in captured.out

def test_calculator_clear_empty(mock_input, capsys):
    mock_input.side_effect = ['clear', 'exit']
    calculator()
    # No output expected for clear on empty history
    captured = capsys.readouterr()
    assert captured.out  # Just ensure it runs without error

def test_calculator_save_empty(mock_input, capsys):
    mock_input.side_effect = ['save', 'exit']
    with patch('app.calculator.save_history') as mock_save:
        calculator()
    mock_save.assert_called_with([])

def test_calculator_load_invalid_csv(tmp_path, mock_input, capsys):
    csv_path = tmp_path / "calculator.csv"
    with open(csv_path, 'w') as f:
        f.write("Invalid,Data\n")
    with patch('app.calculator.open') as m_open:
        m_open.return_value.__enter__.return_value = csv.reader(StringIO("Invalid,Data\n"))
        mock_input.side_effect = ['load', 'exit']
        calculator()
    captured = capsys.readouterr()
    assert "Loaded 0 calculations" in captured.out  # Assuming it skips invalid rows

def test_calculator_multiple_operations(mock_input, capsys):
    mock_input.side_effect = ['add', '1', '2', 'subtract', '5', '3', 'history', 'exit']
    calculator()
    captured = capsys.readouterr()
    assert "1 + 2 = 3" in captured.out
    assert "5 - 3 = 2" in captured.out

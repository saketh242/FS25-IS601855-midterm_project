import pytest
from unittest.mock import patch, mock_open
from io import StringIO
import csv
from app.calculator import calculator, display_history, display_help, save_history, load_history, process_command
from app.calculation import CalculationFactory

@pytest.fixture
def mock_input():
    return patch('builtins.input')

@pytest.fixture
def mock_print(capsys):
    return capsys

def test_process_exit(capsys):
    history = []
    undo_history = []
    assert process_command("exit", history, undo_history) is True
    captured = capsys.readouterr()
    assert "Thank you for using the calculator. Bye!" in captured.out

def test_calculator_add_operation(mock_input, capsys):
    mock_input.side_effect = ['add', '2', '3', 'exit']
    with patch('app.calculator.log_operation') as mock_log:
        history = []
        undo_history = []
        process_command("add", history, undo_history)
    mock_log.assert_called()

def test_calculator_subtract_operation(mock_input, capsys):
    mock_input.side_effect = ['subtract', '5', '3', 'exit']
    history = []
    undo_history = []
    process_command("subtract", history, undo_history)

def test_calculator_multiply_operation(mock_input, capsys):
    mock_input.side_effect = ['multiply', '4', '3', 'exit']
    history = []
    undo_history = []
    process_command("multiply", history, undo_history)

def test_calculator_divide_operation(mock_input, capsys):
    mock_input.side_effect = ['divide', '10', '2', 'exit']
    history = []
    undo_history = []
    process_command("divide", history, undo_history)

def test_process_history_empty(capsys):
    history = []
    undo_history = []
    process_command("history", history, undo_history)
    captured = capsys.readouterr()
    assert "No calculations yet" in captured.out

def test_process_help(capsys):
    process_command("help", [], [])
    captured = capsys.readouterr()
    assert "Help" in captured.out

def test_process_undo(capsys):
    history = [CalculationFactory.register_calculation("add", 1, 2)]
    undo_history = []
    process_command("undo", history, undo_history)
    assert len(history) == 0
    assert len(undo_history) == 1

def test_process_undo_empty(capsys):
    history = []
    undo_history = []
    process_command("undo", history, undo_history)
    captured = capsys.readouterr()
    assert "No history to undo" in captured.out

def test_calculator_history(mock_input, capsys):
    mock_input.side_effect = ['add', '1', '2', 'history', 'exit']
    history = []
    undo_history = []
    process_command("add", history, undo_history)
    process_command("history", history, undo_history)

def test_calculator_help(mock_input, capsys):
    mock_input.side_effect = ['help', 'exit']
    history = []
    undo_history = []
    process_command("help", history, undo_history)

def test_calculator_undo(mock_input, capsys):
    mock_input.side_effect = ['add', '1', '2', 'undo', 'history', 'exit']
    history = []
    undo_history = []
    process_command("add", history, undo_history)
    process_command("undo", history, undo_history)
    process_command("history", history, undo_history)

def test_calculator_redo(mock_input, capsys):
    mock_input.side_effect = ['add', '1', '2', 'undo', 'redo', 'history', 'exit']
    history = []
    undo_history = []
    process_command("add", history, undo_history)
    process_command("undo", history, undo_history)
    process_command("redo", history, undo_history)
    process_command("history", history, undo_history)

def test_calculator_clear(mock_input, capsys):
    mock_input.side_effect = ['add', '1', '2', 'clear', 'history', 'exit']
    history = []
    undo_history = []
    process_command("add", history, undo_history)
    process_command("clear", history, undo_history)
    process_command("history", history, undo_history)

def test_calculator_save_and_load(mock_input, tmp_path):
    csv_path = tmp_path / "calculator.csv"
    with patch('app.calculator.open', mock_open()) as m_open:
        mock_file = StringIO()
        m_open.return_value.__enter__.return_value = mock_file
        mock_input.side_effect = ['add', '1', '2', 'save', 'exit']
        history = []
        undo_history = []
        process_command("add", history, undo_history)
        process_command("save", history, undo_history)
    # Simulate load
    loaded = load_history()
    assert len(loaded) > 0

def test_calculator_invalid_input(mock_input, capsys):
    mock_input.side_effect = ['invalid', 'exit']
    history = []
    undo_history = []
    process_command("invalid", history, undo_history)

def test_calculator_value_error(mock_input, capsys):
    mock_input.side_effect = ['add', 'a', 'exit']
    history = []
    undo_history = []
    process_command("add", history, undo_history)

def test_calculator_zero_division(mock_input, capsys):
    mock_input.side_effect = ['divide', '1', '0', 'exit']
    history = []
    undo_history = []
    process_command("divide", history, undo_history)

def test_calculator_unexpected_error(mock_input, capsys):
    with patch('app.calculation.CalculationFactory.register_calculation') as mock_calc:
        mock_calc.side_effect = Exception("Unexpected")
        mock_input.side_effect = ['add', '1', '2', 'exit']
        history = []
        undo_history = []
        process_command("add", history, undo_history)

def test_save_history(tmp_path):
    calc = CalculationFactory.register_calculation("add", 1, 2)
    csv_path = tmp_path / "calculator.csv"
    with patch('app.calculator.open') as m_open:
        mock_file = StringIO()
        m_open.return_value.__enter__.return_value = mock_file
        save_history([calc])
    # Assert something was written
    assert mock_file.getvalue()

def test_load_history_no_file(tmp_path):
    with patch('app.calculator.open', side_effect=FileNotFoundError):
        loaded = load_history()
        assert loaded == []

def test_load_history_error(tmp_path):
    with patch('app.calculator.open', side_effect=Exception("Error")):
        loaded = load_history()
        assert loaded == []

def test_calculator_save_empty(mock_input, capsys):
    mock_input.side_effect = ['save', 'exit']
    with patch('app.calculator.save_history') as mock_save:
        history = []
        undo_history = []
        process_command("save", history, undo_history)
    mock_save.assert_called_with([])

def test_calculator_load_invalid_csv(tmp_path, mock_input, capsys):
    csv_path = tmp_path / "calculator.csv"
    with open(csv_path, 'w') as f:
        f.write("Invalid,Data\n")
    with patch('app.calculator.open') as m_open:
        m_open.return_value.__enter__.return_value = csv.reader(StringIO("Invalid,Data\n"))
        mock_input.side_effect = ['load', 'exit']
        history = []
        undo_history = []
        process_command("load", history, undo_history)

def test_calculator_multiple_operations(mock_input, capsys):
    mock_input.side_effect = ['add', '1', '2', 'subtract', '5', '3', 'history', 'exit']
    history = []
    undo_history = []
    process_command("add", history, undo_history)
    process_command("subtract", history, undo_history)
    process_command("history", history, undo_history)

def test_process_add_operation(monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda _: '2')
    monkeypatch.setattr('builtins.input', lambda _: '3')  # Note: need sequential mocks
    # Better to use a queue for inputs
    inputs = iter(['2', '3'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    history = []
    undo_history = []
    process_command("add", history, undo_history)
    captured = capsys.readouterr()
    assert "The result is 5" in captured.out
    assert len(history) == 1

def test_process_redo(capsys):
    history = []
    undo_history = [CalculationFactory.register_calculation("add", 1, 2)]
    process_command("redo", history, undo_history)
    assert len(history) == 1
    assert len(undo_history) == 0

def test_process_clear():
    history = [CalculationFactory.register_calculation("add", 1, 2)]
    undo_history = [CalculationFactory.register_calculation("subtract", 5, 3)]
    process_command("clear", history, undo_history)
    assert len(history) == 0
    assert len(undo_history) == 0

def test_process_save(monkeypatch):
    history = [CalculationFactory.register_calculation("add", 1, 2)]
    with patch('app.calculator.save_history') as mock_save:
        process_command("save", history, [])
    mock_save.assert_called_with(history)

def test_process_load(monkeypatch):
    with patch('app.calculator.load_history') as mock_load:
        mock_load.return_value = [CalculationFactory.register_calculation("add", 1, 2)]
        history = []
        process_command("load", history, [])
    assert len(history) == 1

def test_process_invalid(capsys):
    process_command("invalid", [], [])
    captured = capsys.readouterr()
    assert "Invalid input" in captured.out

def test_process_value_error(monkeypatch, capsys):
    inputs = iter(['a', '2'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    process_command("add", [], [])
    captured = capsys.readouterr()
    assert "Enter not a valid number" in captured.out

def test_process_zero_division(capsys):
    with patch('builtins.input', side_effect=['1', '0']):
        process_command("divide", [], [])
    captured = capsys.readouterr()
    assert "You know we cannot divide by zero" in captured.out

def test_process_unexpected_error(monkeypatch, capsys):
    inputs = iter(['1', '2'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('app.calculation.CalculationFactory.register_calculation') as mock_calc:
        mock_calc.side_effect = Exception("Unexpected")
        process_command("add", [], [])
    captured = capsys.readouterr()
    assert "Unexpected error" in captured.out

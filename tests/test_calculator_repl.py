from app.calculator import display_help, display_history, calculator
from app.calculation import AddCalculation


def test_display_help(capsys):
    display_help()
    captured = capsys.readouterr()
    assert 'Type history for history' in captured.out


def test_display_history(capsys):
    history = [AddCalculation(1, 2), AddCalculation(3, 4)]
    display_history(history)
    captured = capsys.readouterr()
    assert 'Calculator history' in captured.out
    assert '+ 2' in captured.out


def test_calculator_exit(monkeypatch, capsys):
    # simulate user entering 'exit' immediately
    inputs = iter(['exit'])
    monkeypatch.setattr('builtins.input', lambda prompt='': next(inputs))
    calculator()
    captured = capsys.readouterr()
    assert 'Welcome to the calculator' in captured.out

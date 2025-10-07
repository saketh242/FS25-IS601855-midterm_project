import pytest
import os
from app.calculator import calculator, display_history, display_help, save_history, load_history
from app.calculation import CalculationFactory

def test_display_history_empty(capsys):
    display_history([])
    captured = capsys.readouterr()
    assert "No calculations yet" in captured.out

def test_display_history_nonempty(capsys):
    calc = CalculationFactory.register_calculation("add", 1, 2)
    display_history([calc])
    captured = capsys.readouterr()
    assert "Calculator history" in captured.out
    assert str(calc) in captured.out

def test_display_help(capsys):
    display_help()
    captured = capsys.readouterr()
    assert "Help" in captured.out
    assert "history" in captured.out
    assert "exit" in captured.out

def test_save_and_load_history(tmp_path):
    calc = CalculationFactory.register_calculation("add", 1, 2)
    # Change working directory to tmp_path for file isolation
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    save_history([calc])
    loaded = load_history()
    os.chdir(old_cwd)
    assert len(loaded) == 1
    assert loaded[0].operation == "add"
    assert loaded[0].a == 1
    assert loaded[0].b == 2

def test_load_history_file_not_found(tmp_path):
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    loaded = load_history()
    os.chdir(old_cwd)
    assert loaded == []

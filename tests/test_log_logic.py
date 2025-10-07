import pytest
from app.log_logic import log_operation, get_log
import os
import logging


def test_get_log_reads_file(tmp_path, monkeypatch):
    log_file = tmp_path / "calculator.log"
    monkeypatch.setattr("app.log_logic.LOG_FILE", str(log_file))
    with open(log_file, "w") as f:
        f.write("hello world\n")
    assert get_log() == "hello world\n"

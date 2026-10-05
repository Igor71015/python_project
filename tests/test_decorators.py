import os
import pytest
from src.decorators import log


def test_log_to_console_success(capsys: pytest.CaptureFixture) -> None:
    """Тест успешного выполнения функции с выводом лога в консоль."""

    @log()
    def add(x: int, y: int) -> int:
        return x + y

    assert add(1, 2) == 3
    captured = capsys.readouterr()
    assert captured.out.strip() == "add ok"


def test_log_to_console_error(capsys: pytest.CaptureFixture) -> None:
    """Тест вывода ошибки функции в консоль."""

    @log()
    def divide(x: int, y: int) -> float:
        return x / y

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    captured = capsys.readouterr()
    assert "divide error: ZeroDivisionError. Inputs: (1, 0), {}" in captured.out.strip()


def test_log_to_file_success() -> None:
    """Тест успешного выполнения функции с записью лога в файл."""
    test_file = "test_success.txt"

    @log(filename=test_file)
    def multiply(x: int, y: int) -> int:
        return x * y

    try:
        assert multiply(2, 3) == 6
        with open(test_file, "r", encoding="utf-8") as f:
            lines = f.read()
        assert lines.strip() == "multiply ok"
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)


def test_log_to_file_error() -> None:
    """Тест записи ошибки функции в файл."""
    test_file = "test_error.txt"

    @log(filename=test_file)
    def raise_value_error() -> None:
        raise ValueError("Неверное значение")

    try:
        with pytest.raises(ValueError):
            raise_value_error()

        with open(test_file, "r", encoding="utf-8") as f:
            lines = f.read()
        assert "raise_value_error error: ValueError. Inputs: (), {}" in lines
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)

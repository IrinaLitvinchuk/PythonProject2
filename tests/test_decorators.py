import os
from typing import Callable

import pytest

from src.decorators import log


# Тест для успешного выполнения
@log
def successful_func(a: int, b: int):
    """Сложение 2х целых чисел"""
    return a + b


def test_log_success(capsys: object) -> Callable:
    """ "Проверка логирования успешной операции и тестирование вывода в консоль"""
    successful_func(1, 2)
    captured = capsys.readouterr()
    assert "successful_func ok \n" in captured.out


# Тест для ошибки
@log()
def failing_func(a: str, b: int):
    """Сложение 2х целых чисел"""
    return a + b  # Будет TypeError при некорректных типах


def test_log_error(capsys):
    """Проверка логирования ошибки типа данных при выводе в консоль"""
    with pytest.raises(TypeError):
        failing_func("1", 2)
    captured = capsys.readouterr()
    assert "failing_func error: TypeError. Inputs: ('1', 2), {} \n" in captured.out


def test_log_in_file() -> None:
    """Тестирует, что декорированная функция корректно пишет логи в файл."""

    @log(filename="test_log.txt")
    def sum_args(a, b):
        return a + b

    sum_args(10, 20)

    # Читаем журнал
    with open("test_log.txt", "r", encoding="utf-8") as file:
        content = file.read()
    assert "sum_args ok \n" in content

    # Удаляем временный файл
    os.remove("test_log.txt")


def test_log_error_zero_divide_in_file() -> None:
    """Проверка логирования ошибки при делении на 0, тестирует запись в файл"""

    @log(filename="test_log.txt")
    def failing_func_divide(a, b):
        return a / b  # обрабатываем ZeroDivisionError при делении на 0

    with pytest.raises(ZeroDivisionError):
        failing_func_divide(2, 0)

    # Читаем журнал
    with open("test_log.txt", "r", encoding="utf-8") as file:
        content = file.read()

    assert "failing_func_divide error: ZeroDivisionError. Inputs: (2, 0), {} \n" in content

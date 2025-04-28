import pytest

from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number(card_number) -> None:
    """Тестирование правильности маскирования номера карты"""
    assert get_mask_card_number(card_number) == "7000 79** **** 6361"


def test_get_mask_card_number_empty():
    """Проверка, что функция корректно обрабатывает входные строки, где отсутствует номер карты"""
    assert get_mask_card_number("") == "Введите номер карты"


def test_get_mask_card_number_wrong_digits() -> None:
    """Проверка, что функция корректно обрабатывает входные строки, если вводится больше или меньше 16 цифр"""
    assert get_mask_card_number("12345") == "Номер карты должен состоять из 16 цифр"
    assert get_mask_card_number("12345678901234567") == "Номер карты должен состоять из 16 цифр"


def test_get_mask_card_number_wrong_type() -> None:
    """Проверка, что функция вызывает исключение TypeError,
       если тип входных данных не соответствует ожидаемому (строка)"""
    with pytest.raises(TypeError):
        get_mask_card_number(7000792289606361)
        get_mask_card_number([7000792289606361])


def test_get_mask_account(account_number) -> None:
    """Тестирование правильности маскирования номера счета"""
    assert get_mask_account(account_number) == "**4305"


def test_get_mask_account_wrong_type() -> None:
    """Проверка, что функция вызывает исключение TypeError,
       если тип входных данных не соответствует ожидаемому (строка)"""
    with pytest.raises(TypeError):
        get_mask_account(73654108430135874305)
        get_mask_account([7, 3, 6, 5])



def test_get_mask_account_wrong_digit_count() -> None:
    """Проверка, что функция корректно обрабатывает входные строки, если вводится больше или меньше 20 цифр"""
    assert get_mask_account("12345") == "Номер счета должен состоять из 20 цифр"


def test_get_mask_account_empty() -> None:
    """Проверка, что функция корректно обрабатывает входные строки, где отсутствует номер счета"""
    assert get_mask_account("") == "Ведите номер счета"

import pytest

from src.widget import get_date, mask_account_card


def test_test_mask_account_card_if_card() -> None:
    """Тест проверяет, корректно ли функция распознает карту и применяет нужный тип маскировки"""
    assert mask_account_card("Visa Platinum 8990922113665229") == "Visa Platinum 8990 92** **** 5229"


def test_test_mask_account_card_if_account() -> None:
    """Тест проверяет, корректно ли функция распознает счет и применяет нужный тип маскировки"""
    assert mask_account_card("Счет 73654108430135874305 ") == "Счет **4305"


@pytest.mark.parametrize(
    "account_or_card_number, expected",
    [
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Счет 35383033474447895560", "Счет **5560"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ],
)
def test_mask_account_card(account_or_card_number: str, expected: str) -> None:
    """Параметризованные тесты с разными типами карт и счетов для проверки универсальности функции"""
    assert mask_account_card(account_or_card_number) == expected


def test_mask_account_card_not_valid() -> None:
    """Тестирование функции на обработку некорректных входных данных. Для карты это 16 цифр, для счета - 20"""
    assert (
        mask_account_card("Счет 12345")
        == """Введен некорректный номер карты или счета.
            Номер карты состоит из 16 цифр.
            Номер счета состоит из 20 цифр"""
    )
    assert (
        mask_account_card("Visa Gold 12345678901234567")
        == """Введен некорректный номер карты или счета.
            Номер карты состоит из 16 цифр.
            Номер счета состоит из 20 цифр"""
    )


def test_mask_account_card_wrong_type() -> None:
    """Тест на обработку некорректного типа данных. Ожидает строку, в противном случае вызывает TypeError"""
    with pytest.raises(TypeError):
        mask_account_card(12345)
        mask_account_card(["Visa", "Gold", 5999414228426353])


def test_get_date(date_input: str) -> None:
    """Тест на правильность преобразования даты"""
    assert get_date(date_input) == "11.03.2024"


def test_get_date_wrong_type() -> None:
    """Тест на обработку некорректного типа данных. Ожидает строку, в противном случае вызывает TypeError"""
    with pytest.raises(TypeError):
        get_date(28042025)


def test_get_date_empty() -> None:
    """Проверка, что функция корректно обрабатывает входные строки, где отсутствует дата"""
    assert get_date("") == "Отсутствует дата. Проверьте корректность входных данных"

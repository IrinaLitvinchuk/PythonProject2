import pytest

from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


def test_filter_by_currency_usd(transactions_list):
    """Тестирование корректной фильтрации по валюте USD"""
    result = list(filter_by_currency(transactions_list, "USD"))
    expected = [
        transaction for transaction in transactions_list if transaction["operationAmount"]["currency"]["code"] == "USD"
    ]
    assert result == expected


def test_empty_list() -> None:
    """Проверка поведения при передаче пустого списка."""
    result = list(filter_by_currency([], "USD"))
    assert result == []


def test_invalid_data_type():
    """показывает ошибку при неверном типе передаваемых данных."""
    invalid_data = ["not a dict"]
    with pytest.raises(TypeError):
        list(filter_by_currency(invalid_data, "USD"))


def test_no_currency(transactions_list_no_currency: list[dict]) -> None:
    """Тест на правильность работы функции, когда отсутствует информация о валюте."""
    result = list(filter_by_currency(transactions_list_no_currency, "USD"))
    expected = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        }
    ]
    assert result == expected


def test_transaction_descriptions(transactions_list_no_description: list[dict]) -> None:
    """Тест на правильность работы функции, когда отсутствует информация об описании."""
    result = list(transaction_descriptions(transactions_list_no_description))
    expected = [transaction.get("description") for transaction in transactions_list_no_description]
    assert result == expected

#  для тестов с параметризацией для функции-генератора номеров карт с различным набором входных данных
@pytest.mark.parametrize(
    "start, stop, expected",
    [
        (
            1,
            5,
            [
                "0000 0000 0000 0001",
                "0000 0000 0000 0002",
                "0000 0000 0000 0003",
                "0000 0000 0000 0004",
                "0000 0000 0000 0005",
            ],
        ),
        (
            1000,
            1005,
            [
                "0000 0000 0000 1000",
                "0000 0000 0000 1001",
                "0000 0000 0000 1002",
                "0000 0000 0000 1003",
                "0000 0000 0000 1004",
                "0000 0000 0000 1005",
            ],
        ),
        # (-1, 1, []),  # Некорректный стартовый индекс
        (
            9999999999999995,
            9999999999999999,
            [
                "9999 9999 9999 9995",
                "9999 9999 9999 9996",
                "9999 9999 9999 9997",
                "9999 9999 9999 9998",
                "9999 9999 9999 9999",
            ],
        ),
        (1, 1, ["0000 0000 0000 0001"]),  # start=stop одинаковые границы
        (9999999999999999, 9999999999999999, ["9999 9999 9999 9999"]),  # Максимальная граница
    ],
)

def test_card_number_generator(start, stop, expected):
    """Тестирование функции-генератора номеров карт с различным набором входных данных"""
    assert list(card_number_generator(start, stop)) == expected

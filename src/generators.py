from typing import Iterator


def filter_by_currency(transactions_list: list[dict], currency: str) -> Iterator[dict]:
    """Функция принимает на вход список словарей, представляющих транзакции, и возвращает итератор,
    который поочередно выдает транзакции, где валюта операции соответствует заданной (например, USD)."""

    filtered_list = iter(filter(lambda x: x["operationAmount"]["currency"]["code"] == currency, transactions_list))
    return filtered_list


# чтобы проверить выполнение функции в этом модуле пришлось добавить сюда список с входными данными.
# Получается,что фикстуры работают только в папке tests?
# или их можно импортировать в src?
transactions_list = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    },
    {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2019-03-23T01:09:46.296404",
        "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 44812258784861134719",
        "to": "Счет 74489636417521191160",
    },
    {
        "id": 895315941,
        "state": "EXECUTED",
        "date": "2018-08-19T04:27:37.904916",
        "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 6831982476737658",
        "to": "Visa Platinum 8990922113665229",
    },
    {
        "id": 594226727,
        "state": "CANCELED",
        "date": "2018-09-12T21:27:25.241689",
        "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод организации",
        "from": "Visa Platinum 1246377376343588",
        "to": "Счет 14211924144426031657",
    },
]

usd_transactions = filter_by_currency(transactions_list, "USD")
for _ in range(2):
    print(next(usd_transactions))


def transaction_descriptions(transaction_list: list[dict]) -> Iterator[dict]:
    """Функция принимает список словарей с транзакциями и возвращает описание каждой операции по очереди."""
    for transaction in transaction_list:
        yield transaction.get("description")


descriptions = transaction_descriptions(transactions_list)
for _ in range(5):
    print(next(descriptions))


def card_number_generator(start: int = 1, stop: int = 9999999999999999) -> Iterator[str]:
    """может сгенерировать номера карт в заданном диапазоне от 0000 0000 0000 0001 до 9999 9999 9999 9999."""
    if start > 0 and stop <= 9999999999999999:  # обрабатывает отрицательное число start и некорректный диапазон
        for number in range(start, stop + 1):
            formatted_card = f"{number:016d}"  # преобразуем в строку длиной ровно 16 символов, дополняя нулями впереди
            new_card = [formatted_card[i: i + 4] for i in range(0, len(formatted_card), 4)]
            yield " ".join(new_card)
    return []  # возвращает пустой список при неправильном диапазоне


for card_number in card_number_generator(1, 5):
    print(card_number)

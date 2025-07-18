import re
from collections import Counter
from typing import List, Any, Dict


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """Функция для поиска в списке словарей операций по заданной строке.
    Принимает список с транзакциями и строку для поиска."""
    pattern = re.compile(search, flags=re.IGNORECASE)

    result_list = []
    for item in data:
        description = item.get("description", "")

        if pattern.search(description):
            result_list.append(item)

    if result_list == []:
        print("Операций, содержащих данное слово, не найдено")

    return result_list


if __name__ == "__main__":
    operations_data = [
        {"id": 1, "amount": 1000, "description": "Оплата товаров"},
        {"id": 2, "amount": 2000, "description": "Перевод другу"},
        {"id": 3, "amount": 3000, "description": "Покупка техники"},
    ]

    # Поиск всех записей, содержащих слово 'товары'
    result = process_bank_search(operations_data, "Товар")
    print(result)


def process_bank_operations(data: List[Dict[Any, Any]], categories: List[str]) -> Dict[str, int]:
    """Функция для подсчета количества банковских операций определенного типа,
    принимает два аргумента: список словарей с данными о банковских операциях и список категорий операций,
    возвращает словарь, в котором ключи — это названия категорий,
    а значения — это количество операций в каждой категории.
    """
    found_categories = []  # Сначала подготовим список категорий, присутствующих в операциях

    for operation in data:
        description = operation.get("description", "")
        for category in categories:
            if category in description:
                found_categories.append(category)
    # Используя Counter считаем частоты встречаемости каждой категории
    category_counts = Counter(found_categories)

    # Переводим Counter обратно в обычный словарь
    results_dict: Dict[str, int] = dict(category_counts)

    return results_dict


if __name__ == "__main__":
    bank_data = [
        {
            "id": 179194306,
            "state": "EXECUTED",
            "date": "2019-05-19T12:51:49.023880",
            "operationAmount": {"amount": "6381.58", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "МИР 5211277418228469",
            "to": "Счет 58518872592028002662",
        },
        {
            "id": 27192367,
            "state": "CANCELED",
            "date": "2018-12-24T20:16:18.819037",
            "operationAmount": {"amount": "991.49", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 71687416928274675290",
            "to": "Счет 87448526688763159781",
        },
        {
            "id": 921286598,
            "state": "EXECUTED",
            "date": "2018-03-09T23:57:37.537412",
            "operationAmount": {"amount": "25780.71", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Счет 26406253703545413262",
            "to": "Счет 20735820461482021315",
        },
        {
            "id": 957763565,
            "state": "EXECUTED",
            "date": "2019-01-05T00:52:30.108534",
            "operationAmount": {"amount": "87941.37", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 46363668439560358409",
            "to": "Счет 18889008294666828266",
        },
        {
            "id": 667307132,
            "state": "EXECUTED",
            "date": "2019-07-13T18:51:29.313309",
            "operationAmount": {"amount": "97853.86", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод с карты на счет",
            "from": "Maestro 1308795367077170",
            "to": "Счет 96527012349577388612",
        },
    ]

    categories = ["Перевод со счета на счет", "Перевод с карты на счет", "Перевод организации"]

    result_dict: Dict[str, int] = process_bank_operations(bank_data, categories)
    print(result_dict)

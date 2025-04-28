from typing import Any


def filter_by_state(transactions: list, state: str = "EXECUTED") -> str | list[Any]:
    """Функция фильтрует список словарей по значению ключа 'state'."""
    filtered_list = []
    for item in transactions:
        if item.get("state") == state:
            filtered_list.append(item)
        elif item.get("state") == "":
            return "Статус операции отсутствует. Проверьте данные"
    return filtered_list


# пример работы функции
# transactions = [
#     {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
#     {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
#     {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
#     {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
# ]
# result = filter_by_state(transactions)  # значение ключа по умолчанию "executed"
# print(result)
# result = filter_by_state(transactions, "CANCELED")
# print(result)


def sort_by_date(transactions: list, reverse: bool = True) -> list:
    """Функция сортирует список словарей по дате, по умолчанию - убывание, т.е. сначала новые даты"""

    # Сначала собираем все даты из словарей
    dates = []
    for element in transactions:
        current_date = element['date']
        dates.append(current_date)

        if all(sep in current_date for sep in ["-", ":", ".", "T"]): # для теста на некорректный формат
            sorted_list = sorted(transactions, key=lambda x: x.get("date"), reverse=reverse)
        else:
            raise ValueError("Некорректно указан формат входных данных")


    counts = {} # Создаем словарь для подсчета частот дат
    for date in dates:
        if date in counts:
            counts[date] += 1
        else:
            counts[date] = 1

    # Проверяем, есть ли повторяющиеся даты
    duplicates = []
    for date, count in counts.items():
        if count > 1:
            duplicates.append(date)

    # Если есть повторяющиеся даты, выдаем ошибку
    if duplicates:
        raise ValueError("Проверьте корректность даты операции: найдены повторяющиеся даты.")

    # Если ошибок нет, выполняем обычную сортировку
    sorted_list = sorted(transactions, key=lambda x: x.get("date"), reverse=reverse)


    return sorted_list


# пример работы функции сортировки
# result = sort_by_date(transactions)  # сортируем даты от новых к старым, по убыванию
# print(result)
#
# result = sort_by_date(transactions, False)  # сортируем даты по возрастанию
# print(result)

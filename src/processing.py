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


def sort_by_date(transactions: list, reverse: bool = True) -> list:
    """Функция сортирует список словарей по дате, по умолчанию - убывание, т.е. сначала новые даты"""

    # Для теста, есть ли повторяющиеся даты, сначала собираем все даты из словарей
    dates = []
    for element in transactions:
        current_date = element["date"]
        dates.append(current_date)

        if not all(sep in current_date for sep in ["-", ":", ".", "T"]):  # для теста на некорректный формат
            raise ValueError("Некорректно указан формат входных данных")

    counts = {}  # Создаем словарь для подсчета частот дат
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

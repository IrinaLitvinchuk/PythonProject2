from typing import Any, List, Dict
from datetime import datetime
import re

import pandas as pd


def filter_by_state(transactions: list, state: str = "EXECUTED") -> str | list[Any]:
    """Функция фильтрует список словарей по значению ключа 'state'."""
    filtered_list = []
    for item in transactions:
        if item.get("state") == state:
            filtered_list.append(item)
        elif item.get("state") == "":
            return "Статус операции отсутствует. Проверьте данные"
    return filtered_list


def convert_to_datetime(value):
    """Преобразует любое значение в объект datetime.
       Поддерживает: строки разных форматов, объекты pandas.Timestamp, None-значения."""
    if isinstance(value, datetime):
        return value
    elif isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace("Z", ""))
        except ValueError:
            raise ValueError(f"Невозможно распознать формат даты: '{value}'")
    elif value is None or pd.isna(value):
        return None
    else:
        raise ValueError(f"Неподдерживаемый тип значения даты: {type(value)}")


def sort_by_date(data: List[Dict], field_name: str = 'date', reverse: bool = False) -> List[Dict]:
    """
    Универсально сортирует список словарей по указанному полю с датой.
    Работает с разными форматами ввода (json, csv, xlsx).
    :param data: Список словарей с информацией.
    :param field_name: Название поля с датой ('date' по умолчанию).
    :param reverse: Сортируем по возрастанию (False) или убыванию (True, по умолчанию).
    :return: Отсортированный список словарей.
    """
    # Применяем нашу функцию преобразования ко всем элементам перед сортировкой
    converted_data = [(convert_to_datetime(item[field_name]), item) for item in data]
    # Выполняем сортировку по первому элементу кортежа (объекту datetime)
    sorted_data = sorted(converted_data, key=lambda x: x[0], reverse=reverse)
    # Возвращаем отсортированные словари
    return [item[1] for item in sorted_data]


# def sort_by_date(transactions: list, reverse: bool = True) -> list:
#     """Функция сортирует список словарей по дате, по умолчанию - убывание, т.е. сначала новые даты"""
#
#     # Вспомогательная функция для распознавания формата даты
#     def parse_date(date_str):
#         formats = [
#             "%Y-%m-%dT%H:%M:%S.%f",  # Добавляем этот формат для обработки дат с миллисекундами
#             "%Y-%m-%dT%H:%M:%SZ",
#             "%Y-%m-%d %H:%M:%S",
#             "%d/%m/%Y",
#             "%d.%m.%Y"
#         ]
#         for fmt in formats:
#             try:
#                 return datetime.strptime(date_str, fmt)
#             except ValueError:
#                 continue
#         raise ValueError(f"Не удалось распознать формат даты: {date_str}")
#
#     # Проверяем каждую дату на валидный формат
#     invalid_dates = []
#     for element in transactions:
#         current_date = element.get("date")
#         try:
#             # Пробуем конвертировать дату в объект datetime
#             datetime.fromisoformat(current_date.replace("Z", "+00:00"))
#         except (ValueError, TypeError):
#             invalid_dates.append(current_date)
#
#     if invalid_dates:
#         raise ValueError(f"Проверьте корректность даты операции: обнаружены некорректные даты {invalid_dates}")
#
#     # Для теста, есть ли повторяющиеся даты, сначала собираем все даты из словарей
#     dates = []
#     for element in transactions:
#         current_date = element["date"]
#         dates.append(current_date)
#
#         if not all(sep in current_date for sep in ["-", ":", ".", "T"]):  # для теста на некорректный формат
#             raise ValueError("Некорректно указан формат входных данных")
#
#     counts: dict = {}  # Создаем словарь для подсчета частот дат
#     for date in dates:
#         if date in counts:
#             counts[date] += 1
#         else:
#             counts[date] = 1
#
#     # Проверяем, есть ли повторяющиеся даты
#     duplicates = []
#     for date, count in counts.items():
#         if count > 1:
#             duplicates.append(date)
#
#     # Если есть повторяющиеся даты, выдаем ошибку
#     if duplicates:
#         raise ValueError("Проверьте корректность даты операции: найдены повторяющиеся даты.")
#
#
#
#     #Если ошибок нет, выполняем обычную сортировку
#     sorted_list = sorted(transactions, key=lambda t: parse_date(t.get('date')), reverse=reverse)
#     return sorted_list

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
       Поддерживает строки разных форматов, объекты pandas.Timestamp, None-значения."""
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



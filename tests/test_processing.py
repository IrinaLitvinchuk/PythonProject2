from datetime import datetime

import pandas as pd
import pytest

from src.processing import convert_to_datetime, filter_by_state, sort_by_date


def test_filter_by_state(transactions: list) -> None:
    """Тестирование фильтрации списка словарей по заданному статусу state (по умолчанию=EXECUTED)"""
    assert filter_by_state(transactions) == [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]


def test_filter_by_state_no_state() -> None:
    """Проверка работы функции при отсутствии словарей с указанным статусом state в списке"""
    assert (
        filter_by_state(
            [
                {"id": 41428829, "state": "", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "", "date": "2018-10-14T08:21:33.419441"},
            ]
        )
        == "Статус операции отсутствует. Проверьте данные"
    )


@pytest.mark.parametrize(
    "state, expected",
    [
        (
            "EXECUTED",
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
        ),
        (
            "CANCELED",
            [
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
        ),
    ],
)
def test_filter_by_state_different_state(transactions: list, state: str, expected: list) -> None:
    """Параметризация тестов для различных возможных значений статуса state"""
    assert filter_by_state(transactions, state) == expected


def test_convert_to_datetime_valid_format():
    """Базовый тест для правильной строки формата ISO"""
    iso_date = "2023-04-15T12:30:00"
    expected = datetime(2023, 4, 15, 12, 30)
    result = convert_to_datetime(iso_date)
    assert result == expected


def test_convert_to_datetime_utc_z():
    """Тест для строки с суффиксом Z (формат UTC)"""
    utc_date = "2023-04-15T12:30:00Z"
    expected = datetime(2023, 4, 15, 12, 30)
    result = convert_to_datetime(utc_date)
    assert result == expected


def test_convert_to_datetime_pandas_timestamp():
    """Тест для объекта pandas.Timestamp"""
    timestamp = pd.Timestamp("2023-04-15 12:30:00")
    expected = datetime(2023, 4, 15, 12, 30)
    result = convert_to_datetime(timestamp)
    assert result == expected


def test_convert_to_datetime_none():
    """Тест для пропуска (None-значение)"""
    result = convert_to_datetime(None)
    assert result is None


def test_convert_to_datetime_nan():
    """Тест для NaN-значения"""
    nan_value = float("nan")
    result = convert_to_datetime(nan_value)
    assert result is None


def test_convert_to_datetime_invalid_format():
    """Тест для неправильного формата даты"""
    bad_date = "not a date"
    with pytest.raises(ValueError):
        convert_to_datetime(bad_date)


def test_convert_to_datetime_unsupported_type():
    """Тест для неподдерживаемых типов данных"""
    int_value = 12345
    with pytest.raises(ValueError):
        convert_to_datetime(int_value)


def test_convert_to_datetime_empty_string():
    """Тест для пограничного случая (пустая строка)"""
    empty_string = ""
    with pytest.raises(ValueError):
        convert_to_datetime(empty_string)


def test_sort_by_date_ascending():
    """Сортировка по возрастанию"""
    data = [
        {"date": "2023-04-15T12:30:00"},
        {"date": "2023-04-16T12:30:00"},
        {"date": "2023-04-14T12:30:00"},
    ]
    expected_dates = ["2023-04-14T12:30:00", "2023-04-15T12:30:00", "2023-04-16T12:30:00"]
    sorted_data = sort_by_date(data)
    dates = [d["date"] for d in sorted_data]
    assert dates == expected_dates


def test_sort_by_date_descending():
    """Сортировка по убыванию"""
    data = [
        {"date": "2023-04-15T12:30:00"},
        {"date": "2023-04-16T12:30:00"},
        {"date": "2023-04-14T12:30:00"},
    ]
    expected_dates = ["2023-04-16T12:30:00", "2023-04-15T12:30:00", "2023-04-14T12:30:00"]
    sorted_data = sort_by_date(data, reverse=True)
    dates = [d["date"] for d in sorted_data]
    assert dates == expected_dates

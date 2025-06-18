from unittest import mock
from unittest.mock import patch

import pandas as pd

from src.transaction_reader import read_transactions_from_csv, read_transactions_from_excel


def test_read_csv_success():
    """Проверяем успешное считывание данных из CSV"""
    with mock.patch("pandas.read_csv") as mock_read_csv:
        test_df = pd.DataFrame(
            {
                "id": [650703, 3598919],
                "state": ["EXECUTED", "EXECUTED"],
                "date": ["2023-09-05T11:30:32Z", "2020-12-06T23:00:58Z"],
                "amount": [16210, 29740],
                "currency_name": ["Sol", "Peso"],
                "currency_code": ["PEN", "COP"],
                "from": ["Счет 58803664561298323391", "Discover 3172601889670065"],
                "to": ["Счет 39745660563456619397", "Discover 0720428384694643"],
                "description": ["Перевод организации", "Перевод с карты на карту"],
            }
        )
        mock_read_csv.return_value = test_df
        expected_output = [
            {
                "id": 650703,
                "state": "EXECUTED",
                "date": "2023-09-05T11:30:32Z",
                "amount": 16210,
                "currency_name": "Sol",
                "currency_code": "PEN",
                "from": "Счет 58803664561298323391",
                "to": "Счет 39745660563456619397",
                "description": "Перевод организации",
            },
            {
                "id": 3598919,
                "state": "EXECUTED",
                "date": "2020-12-06T23:00:58Z",
                "amount": 29740,
                "currency_name": "Peso",
                "currency_code": "COP",
                "from": "Discover 3172601889670065",
                "to": "Discover 0720428384694643",
                "description": "Перевод с карты на карту",
            },
        ]
        actual_output = read_transactions_from_csv("fake_file.csv")
        assert actual_output == expected_output, f"Expected {expected_output}, but got {actual_output}"


@patch("pandas.read_csv")
def test_csv_file_not_found(mock_read_csv):
    """Проверяем, что при отсутствии файла возвращается пустой список и печатается сообщение"""
    mock_read_csv.side_effect = FileNotFoundError
    with mock.patch("builtins.print") as mock_print:
        result = read_transactions_from_csv("nonexistent_file.csv")
        assert result == []
        mock_print.assert_called_with("Файл nonexistent_file.csv не найден.")


def test_csv_exception():
    """Симулируем любую другую ошибку при чтении CSV, например, неверный формат"""
    with (
        mock.patch("pandas.read_csv", side_effect=ValueError("Некорректный формат CSV")),
        mock.patch("builtins.print") as mock_print,
    ):
        result = read_transactions_from_csv("invalid.csv")
        assert result == []
        mock_print.assert_called_with("Произошла ошибка: Некорректный формат CSV")


# Пример данных, которые может вернуть read_excel
mock_data = [
    {
        "id": 650703,
        "state": "EXECUTED",
        "date": "2023-09-05T11:30:32Z",
        "amount": 16210,
        "currency_name": "Sol",
        "currency_code": "PEN",
        "from": "Счет 58803664561298323391",
        "to": "Счет 39745660563456619397",
        "description": "Перевод организации",
    },
    {
        "id": 3598919,
        "state": "EXECUTED",
        "date": "2020-12-06T23:00:58Z",
        "amount": 29740,
        "currency_name": "Peso",
        "currency_code": "COP",
        "from": "Discover 3172601889670065",
        "to": "Discover 0720428384694643",
        "description": "Перевод с карты на карту",
    },
]


@patch("pandas.read_excel")
def test_read_excel_success(mock_read_excel):
    """Проверяем успешное считывание данных из Excel"""
    mock_df = pd.DataFrame(mock_data)
    mock_read_excel.return_value = mock_df
    result = read_transactions_from_excel("fake_file.xlsx")

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["id"] == 650703
    mock_read_excel.assert_called_once_with("fake_file.xlsx")


@patch("pandas.read_excel")
def test_read_excel_file_not_found(mock_read_excel):
    """Проверяем, что при отсутствии файла возвращается пустой список и печатается сообщение"""
    mock_read_excel.side_effect = FileNotFoundError
    with mock.patch("builtins.print") as mock_print:
        result = read_transactions_from_excel("nonexistent_file.xlsx")
        assert result == []
        mock_print.assert_called_with("Файл nonexistent_file.xlsx не найден.")


@patch("pandas.read_excel")
def test_excel_exception(mock_read_excel):
    """Симулируем любую другую ошибку при чтении Excel, например, неверный формат"""
    with (
        mock.patch("pandas.read_excel", side_effect=ValueError("Некорректный формат Excel")),
        mock.patch("builtins.print") as mock_print,
    ):
        result = read_transactions_from_excel("invalid_file.xlsx")
        assert result == []
        mock_print.assert_called_with("Произошла ошибка: Некорректный формат Excel")

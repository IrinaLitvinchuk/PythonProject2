import json
from unittest import mock
from unittest.mock import mock_open, patch

from src.utils import get_transactions


@patch("os.path.isfile", return_value=True)
@patch("builtins.open", new_callable=mock_open, read_data='[{"id": 1}, {"id": 2}]')
def test_get_transactions_correct(mock_open, mock_isfile):
    """Тестирование корректной работы функции"""
    path = "/correct/path/to/file.json"
    expected_result = [{"id": 1}, {"id": 2}]
    actual_result = get_transactions(path)
    assert actual_result == expected_result


@mock.patch("builtins.open", side_effect=FileNotFoundError)
def test_file_not_found(mock_open):
    """Обработка ошибки, когда файл не найден"""
    result = get_transactions("fake_path.json")
    assert result == []


@mock.patch("builtins.open", new_callable=mock.mock_open, read_data="invalid json")
@mock.patch("json.load", side_effect=json.JSONDecodeError("Invalid syntax", "", 0))
def test_invalid_json(mock_json_load, mock_open):
    """Обработка ошибки, когда файл содержит неправильный JSON"""
    result = get_transactions("fake_path.json")
    assert result == []


@mock.patch("builtins.open", new_callable=mock.mock_open, read_data="")
@mock.patch("json.load", side_effect=json.JSONDecodeError("Empty file", "", 0))
def test_empty_file(mock_json_load, mock_open):
    """Обработка ошибки, когда файл пустой"""
    result = get_transactions("empty_file.json")
    assert result == []

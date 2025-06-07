import json
from typing import Callable, Dict, List
from unittest import mock
from unittest.mock import Mock, mock_open, patch

from src.utils import get_transactions


@patch("os.path.isfile", return_value=True)
@patch("builtins.open", new_callable=mock_open, read_data='[{"id": 1}, {"id": 2}]')
def test_get_transactions_correct(mock_open: Mock, mock_isfile: Mock) -> None:
    """Тестирование корректной работы функции"""
    path = "/correct/path/to/file.json"
    expected_result: List[Dict[str, int]] = [{"id": 1}, {"id": 2}]
    actual_result = get_transactions(path)
    assert actual_result == expected_result


@mock.patch("builtins.open", side_effect=FileNotFoundError)
def test_file_not_found(mock_open: Mock) -> None:
    """Обработка ошибки, когда файл не найден"""
    result = get_transactions("fake_path.json")
    assert result == []


@mock.patch("builtins.open", new_callable=mock.mock_open, read_data="invalid json")
@mock.patch("json.load", side_effect=json.JSONDecodeError("Invalid syntax", "", 0))
def test_json_decode_error(mock_json_load: Callable[[], None], mock_open: Mock) -> None:
    """Обработка ошибки, когда файл не содержит список"""
    result = get_transactions("fake_path.json")
    assert result == []


@patch("os.path.isfile", return_value=True)
@patch("builtins.open", new_callable=mock_open, read_data="{'key': 'value')")
def test_get_transactions__(mock_open: Mock, mock_isfile: Mock) -> None:
    """Обработка ошибки декодирования"""
    file = "test_file.json"
    result = get_transactions(file)
    assert result == []

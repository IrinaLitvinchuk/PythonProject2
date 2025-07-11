import pytest
from unittest.mock import patch
from main import greet_and_choose_file, filter_by_status

def test_greet_and_choose_file_json():
    """Заменяем input с выбором JSON-файла"""
    with patch('builtins.input', side_effect=['1']):
        result = greet_and_choose_file()
        assert result[0] == 'json'

def test_greet_and_choose_file_csv():
    """Заменяем input с выбором CSV-файла"""
    with patch('builtins.input', side_effect=['2']):
        result = greet_and_choose_file()
        assert result[0] == 'csv'

def test_greet_and_choose_file_excel():
    """Заменяем input с выбором Excel-файла"""
    with patch('builtins.input', side_effect=['3']):
        result = greet_and_choose_file()
        assert result[0] == 'excel'

def test_greet_and_choose_file_invalid_option(capsys):
    """Симулируем ввод несуществующего пункта меню"""
    with patch('builtins.input', side_effect=['4', '4', '4']):
        result = greet_and_choose_file()
        assert result == (None, None)  # функция возвращает None при превышении попыток

    # Только после выполнения функции вызываем capsys
    captured = capsys.readouterr()
    assert "Данный пункт меню: 4 отсутствует" in captured.out


def test_filter_by_status():
    # Подготавливаем тестовые данные
    mock_data = [
        {'state': 'EXECUTED'},
        {'state': 'CANCELED'},
        {'state': 'PENDING'}
    ]

    # Заменяем input() на фиктивное значение "EXECUTED"
    with patch('builtins.input', return_value="EXECUTED"):
        result = filter_by_status(mock_data)
        assert len(result) > 0
        assert all(txn['state'] == 'EXECUTED' for txn in result)

    # Проверим другой статус, например "CANCELED"
    with patch('builtins.input', return_value="CANCELED"):
        result = filter_by_status(mock_data)
        assert len(result) > 0
        assert all(txn['state'] == 'CANCELED' for txn in result)

    def test_filter_by_status_invalid():
        mock_data = [
            {'state': 'EXECUTED'},
            {'state': 'CANCELED'},
            {'state': 'PENDING'}
        ]

        # Вводим заведомо неверный статус
        with patch('builtins.input', return_value="UNKNOWN"):
            result = filter_by_status(mock_data)
            assert len(result) == 0  # Должно вернуть пустой список, так как статус неизвестен


def test_filter_by_status_invalid():
    mock_data = [
        {'state': 'EXECUTED'},
        {'state': 'CANCELED'},
        {'state': 'PENDING'}
    ]

    # Вводим заведомо неверный статус
    with patch('builtins.input', return_value="UNKNOWN"):
        result = filter_by_status(mock_data)
        assert len(result) == 0  # Должно вернуть пустой список, так как статус неизвестен
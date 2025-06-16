from unittest import mock
import pandas as pd

from src.transaction_reader import read_transactions_from_csv


def read_financial_operations_from_csv(param):
    pass


def test_read_csv_success():
    """Проверяем успешное считывание данных"""
    with mock.patch('pandas.read_csv') as mock_read_csv:
        test_df = pd.DataFrame({
            'id': [650703, 3598919],
            'state': ['EXECUTED', 'EXECUTED'],
            'date': ['2023-09-05T11:30:32Z', '2020-12-06T23:00:58Z'],
            'amount': [16210, 29740],
            'currency_name': ['Sol', 'Peso'],
            'currency_code': ['PEN', 'COP'],
            'from': ['Счет 58803664561298323391', 'Discover 3172601889670065'],
            'to': ['Счет 39745660563456619397', 'Discover 0720428384694643'],
            'description': ['Перевод организации', 'Перевод с карты на карту']
        })
        mock_read_csv.return_value = test_df
        expected_output = [
            {
                'id': 650703,
                'state': 'EXECUTED',
                'date': '2023-09-05T11:30:32Z',
                'amount': 16210,
                'currency_name': 'Sol',
                'currency_code': 'PEN',
                'from': 'Счет 58803664561298323391',
                'to': 'Счет 39745660563456619397',
                'description': 'Перевод организации'
            },
            {
                'id': 3598919,
                'state': 'EXECUTED',
                'date': '2020-12-06T23:00:58Z',
                'amount': 29740,
                'currency_name': 'Peso',
                'currency_code': 'COP',
                'from': 'Discover 3172601889670065',
                'to': 'Discover 0720428384694643',
                'description': 'Перевод с карты на карту'
            }
        ]
        actual_output = read_transactions_from_csv('fake_file.csv')
        assert actual_output == expected_output, f"Expected {expected_output}, but got {actual_output}"


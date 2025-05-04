import pytest

from src.generators import filter_by_currency, transaction_descriptions, card_number_generator

def test_filter_by_currency_usd(transactions_list):
    """Тестирование корректной фильтрации по валюте USD"""

    expected_transactions = [
            transaction for transaction in transactions_list if
            transaction.get('operationAmount').get('currency').get('code') == 'USD'
        ]
    actual_result = list(filter_by_currency(transactions_list, 'USD'))
    assert actual_result == expected_transactions


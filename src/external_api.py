import os
from typing import Optional, cast

import requests
from dotenv import load_dotenv

from src.utils import get_transactions

load_dotenv()
API_KEY = os.getenv("API_KEY")


def get_converted_amount(transaction: dict) -> Optional[float]:
    """Принимает на вход транзакцию и возвращает сумму транзакции в рублях.
    Если валюта RUB, сумма сразу выводится без конвертации. Если USD или EUR,
    происходит обращение к внешнему API."""
    to_currency = "RUB"
    amount = transaction.get('operationAmount', {}).get('amount', '')
    currency_code = transaction.get('operationAmount', {}).get('currency', {}).get('code', '')

    if currency_code in ["USD", "EUR"]:
        try:
            url = (
                f"https://api.apilayer.com/exchangerates_data/convert?to={to_currency}&from={currency_code}"
                f"&amount={amount}"
            )
            headers = {"apikey": API_KEY}
            response = requests.request("GET", url, headers=headers)

            if response.status_code != 200:
                raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

            data = response.json()
            result = cast(float, data["result"])  # Ясно говорим mypy, что это float
            return result

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}. Please try again later.")
            return None
    else:
        return float(amount)  # Преобразование в float, чтобы соответствовать типу функции


# path = "data/operations.json"
# transactions_info = get_transactions(path)
#
# for transaction in transactions_info:
#     converted_amount = get_converted_amount(transaction)
#     if converted_amount is not None:
#         print(converted_amount)

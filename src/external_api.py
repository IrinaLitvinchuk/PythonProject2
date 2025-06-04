import os
import json
import requests
from utils import get_transactions
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')


def get_converted_amount(transaction: dict) -> float:
    """
    Принимает на вход транзакцию и возвращает сумму транзакции в рублях.
    Если валюта RUB, сумма сразу выводится без конвертации.Если USD или EUR,
    происходит обращение к внешнему API.
    """
    to_currency = 'RUB'
    amount = transaction['operationAmount']['amount']
    currency_code = transaction['operationAmount']['currency']['code']

    if currency_code in ['USD', 'EUR']:
        try:
            url = f"https://api.apilayer.com/exchangerates_data/convert?to={to_currency}&from={currency_code}&amount={amount}"
            headers = {"apikey": API_KEY}
            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

            data = response.json()
            return data['result']

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}. Please try again later.")
            return None
    else:
        return amount


path = 'data/operations.json'
transactions_info = get_transactions(path)

for transaction in transactions_info:
    converted_amount = get_converted_amount(transaction)
    if converted_amount is not None:
        print(converted_amount)



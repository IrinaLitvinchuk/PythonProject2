import os

import requests
from utils import get_transactions
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')

def get_converted_amount(transactions_info: list) -> float:
    """ принимает на вход транзакции и возвращает сумму транзакции в рублях"""
    for transaction in transactions_info:

        to = 'RUB'
        from_usd = 'USD'
        from_eur = 'EUR'
        amount = transaction['operationAmount']['amount']
        payload = {}
        headers= {
          "apikey": f"{API_KEY}"
        }
        if transaction['operationAmount']['currency']['code'] == 'USD':
            url = f"https://api.apilayer.com/exchangerates_data/convert?to={to}&from={from_usd}&amount={amount}"
            response = requests.request("GET", url, headers=headers, data = payload)
            status_code = response.status_code
            result = response.text
            print(status_code)
            print(result)
        elif transaction['operationAmount']['currency']['code'] == 'EUR':
            url = f"https://api.apilayer.com/exchangerates_data/convert?to={to}&from={from_eur}&amount={amount}"
            response = requests.request("GET", url, headers=headers, data = payload)
            status_code = response.status_code
            result = response.text
            print(result)
        elif transaction['operationAmount']['currency']['code'] == 'RUB':
            result = transaction['operationAmount']['amount']
            print(result)



path = 'data/operations.json'
transactions = get_transactions(path)
get_converted_amount(transactions)

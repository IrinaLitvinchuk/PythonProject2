import os
import json

import requests
from utils import get_transactions
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')


def get_converted_amount(transaction: dict) -> float:
    """ принимает на вход транзакци и возвращает сумму транзакции в рублях"""
    to = 'RUB'
    usd = 'USD'
    eur = 'EUR'
    amount = transaction['operationAmount']['amount']

    if transaction['operationAmount']['currency']['code'] == 'USD':
        url = f"https://api.apilayer.com/exchangerates_data/convert?to={to}&from={usd}&amount={amount}"

        headers = {
            "apikey": f"{API_KEY}"
        }
        response = requests.request("GET", url, headers=headers)
        status_code = response.status_code
        if status_code == 200:
            try:
                result = response.json()
                return result["result"]
            except requests.exceptions.RequestException as e:
                print(f"An error occurred {e}. Please try again later.")
                return None

    elif transaction['operationAmount']['currency']['code'] == 'EUR':
        url = f"https://api.apilayer.com/exchangerates_data/convert?to={to}&from={eur}&amount={amount}"
        payload = {}
        headers = {
            "apikey": API_KEY
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        status_code = response.status_code
        if status_code == 200:
            try:
                result = response.json()
                return result["result"]
            except requests.exceptions.RequestException as e:
                print(f"An error occurred {e}. Please try again later.")
                return None


    elif transaction['operationAmount']['currency']['code'] == 'RUB':
        result = transaction['operationAmount']['amount']
        print(result)



path = 'data/operations.json'
transactions_info = get_transactions(path)

for transaction in transactions_info:
    result = get_converted_amount(transaction)



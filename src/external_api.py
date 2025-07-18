import os
from typing import Optional, cast

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")


def get_converted_amount(transaction: dict, use_mock: bool = False) -> Optional[float]:
    """Принимает на вход транзакцию и возвращает сумму транзакции в рублях.
    Если валюта RUB, сумма сразу выводится без конвертации. Если USD или EUR,
    происходит обращение к внешнему API. В режиме тестирования (use_mock=True) API не вызывается."""
    to_currency = "RUB"

    # Сначала проверяем, есть ли вложенная структура operationAmount
    if 'operationAmount' in transaction:
        amount = transaction.get('operationAmount', {}).get('amount', '')
        currency_code = transaction.get('operationAmount', {}).get('currency', {}).get('code', '')
    else:
        # Иначе берем сумму и валюту напрямую
        amount = transaction.get('amount', '')
        currency_code = transaction.get('currency_code', '')

    # Преобразуем сумму в float, если она доступна
    if amount == '':
        return None
    amount_float = float(amount)

    if use_mock:
        # Режим тестирования:
        return None # Ничего не возвращаем, так как side_effect в тестах подставит значение
    else:
        # Обычный режим работы: обращаемся к API
        if currency_code in ["USD", "EUR"]:  # Если валюта подлежит конвертации
            try:
                url = (
                    f"https://api.apilayer.com/exchangerates_data/convert?"
                    f"to={to_currency}&from={currency_code}&amount={amount_float:.2f}"  # округлим до двух знаков после запятой
                )
                headers = {"apikey": API_KEY}
                response = requests.request("GET", url, headers=headers)

                if response.status_code != 200:
                    raise Exception(f"Запрос завершился неудачей с кодом статуса {response.status_code}: {response.text}")

                data = response.json()
                result = float(data["result"])
                return result

            except requests.exceptions.RequestException as e:
                print(f"Произошла ошибка: {e}. Повторите попытку позднее.")
                return None
        else:
            return amount_float  # Если валюта уже в рублях, возвращаем сумму без изменений


# path = "data/operations.json"
# transactions_info = get_transactions(path)
#
# for transaction in transactions_info:
#     converted_amount = get_converted_amount(transaction)
#     if converted_amount is not None:
#         print(converted_amount)

import json


def get_transactions(path: str) -> list[dict]:
    """принимает на вход путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях"""
    try:
        with open(path, encoding="utf-8") as f:
            transactions_info = json.load(f)
        return transactions_info
    except FileNotFoundError:
        print("Файл не найден")
        return []
    except json.JSONDecodeError:
        print("Ошибка декодирования файла")
        return []


# path = 'data/operations.json'
# print(get_transactions(path))


# def transaction_amount(transactions: list) -> float:
#     """ принимает на вход транзакции и возвращает сумму транзакции в рублях"""
#     for transaction in transactions:
#         if transaction['operationAmount']['currency']['code'] == 'RUB':
#             print(transaction['operationAmount']['amount'])
#         elif transaction['operationAmount']['currency']['code'] == 'USD':
#             print('Валюта не найдена')
#         else:
#             pass
#
#
#
#
# transactions = get_transactions(path)
# transaction_amount(transactions)

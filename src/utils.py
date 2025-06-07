import json
from typing import Dict, List, cast


def get_transactions(path: str) -> List[Dict]:
    """принимает на вход путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях"""
    try:
        with open(path, encoding="utf-8") as f:
            transactions_info = cast(List[Dict], json.load(f))  # явно приводим к списку словарей
        return transactions_info
    except FileNotFoundError:
        print("Файл не найден")
        return []
    except json.JSONDecodeError:
        print("Ошибка декодирования файла")
        return []


path = "data/operations.json"
print(get_transactions(path))

import json
import logging
from typing import Dict, List, cast

utils_logger = logging.getLogger("utils_logger")
file_handler = logging.FileHandler("../logs/utils.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
utils_logger.addHandler(file_handler)
utils_logger.setLevel(logging.DEBUG)


def get_transactions(path: str) -> List[Dict]:
    """принимает на вход путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях"""
    utils_logger.info(f"Получен путь до файла {path}")
    try:
        with open(path, encoding="utf-8") as f:
            transactions_info = cast(List[Dict], json.load(f))  # явно приводим к списку словарей
        utils_logger.info("Получен список словарей с данными о финансовых транзакциях")
        return transactions_info
    except FileNotFoundError:
        utils_logger.error("Файл не найден")
        print("Файл не найден")
        return []
    except json.JSONDecodeError:
        utils_logger.error("Ошибка декодирования файла. Файл пустой, либо содержит не список")
        print("Ошибка декодирования файла")
        return []


path = "data/operations.json"  # успешный случай
print(get_transactions(path))

path = "data/operation.json"  # файл не найден
print(get_transactions(path))

path = "data/test_path.json"  # не список
print(get_transactions(path))

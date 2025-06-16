import pandas as pd
import openpyxl


def read_transactions_from_csv(file_path: str) -> list[dict]:
    """Функция считывает финансовые операции из файла CSV и возвращает список словарей"""
    try:
        df = pd.read_csv(file_path, delimiter=';')
        # print(df.shape)
        # print(df.head(3))
        transactions_list = df.to_dict(orient='records')
        return transactions_list

    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return []
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []


if __name__ == '__main__':
    list_transactions = read_transactions_from_csv("data/transactions.csv")
    print(list_transactions)


def read_transactions_from_excel(file_path: str) -> list[dict]:
    """Функция считывает финансовые операции из файла Excel и возвращает список словарей"""
    try:
        df = pd.read_excel(file_path)
        # print(df.shape)
        # print(df.head(3))
        transactions_list = df.to_dict(orient='records')
        return transactions_list

    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return []
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []


if __name__ == '__main__':
    list_transactions = read_transactions_from_excel("data/transactions_excel.xlsx")
    print(list_transactions)
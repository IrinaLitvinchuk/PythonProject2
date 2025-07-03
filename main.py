from src.transaction_reader import read_transactions_from_csv, read_transactions_from_excel
from src.utils import get_transactions
from src.processing import filter_by_state, sort_by_date


def main():
    """"Функция отвечает за основную логику проекта и связывает функциональности между собой."""

    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    while True:
        print("""Выберите необходимый пункт меню:
    1. Получить информацию о транзакциях из JSON-файла
    2. Получить информацию о транзакциях из CSV-файла
    3. Получить информацию о транзакциях из XLSX-файла"
        """)
        choose_file = input()

        if choose_file == '1':
            print('Для обработки выбран JSON-файл.')
            result_json = get_transactions(r'C:\Users\Irina Litvinchuk\PycharmProjects\PythonProject2\src\data\operations.json')
            #print(result_json)
            #return result_json
            break

        elif choose_file == '2':
            print('Для обработки выбран CSV-файл.')
            result_csv = read_transactions_from_csv(r'C:\Users\Irina Litvinchuk\PycharmProjects\PythonProject2\src\data\transactions.csv')
            #print(result_csv)
            #return result_csv
            break


        elif choose_file == '3':
            print('Для обработки выбран XLSX-файл.')
            result_excel = read_transactions_from_excel(r'C:\Users\Irina Litvinchuk\PycharmProjects\PythonProject2\src\data\transactions_excel.xlsx')
            #print(result_excel)
            #return result_excel
            break

        else:
            print(f'Данный пункт меню: {choose_file} отсутствует')
            continue

    while True:
        print("""Введите статус, по которому необходимо выполнить фильтрацию. 
Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING""")
        choose_status = input().upper()
        if choose_status in ["EXECUTED", "CANCELED", "PENDING"]:
            print(f'Операции отфильтрованы по статусу {choose_status}')
            break
        else:
            print(f'Статус операции {choose_status} недоступен.')
            continue

    if choose_file == '1':
        result = filter_by_state(result_json, state=f'{choose_status}')
        print(result)
    elif choose_file == '2':
        result = filter_by_state(result_csv, state=f'{choose_status}')
        print(result)

    elif choose_file == '3':
        result = filter_by_state(result_excel, state=f'{choose_status}')
        print(result)

    while True:
        print('Отсортировать операции по дате? ')
        choose_sort_by_date = input('Да/Нет').upper()
        if choose_sort_by_date == 'Да':
            print('Отсортировать по возрастанию или по убыванию?')
            choose_ascend_descend = input('по возрастанию/по убыванию').lower()
            if choose_ascend_descend == 'по возрастанию':
                result = sort_by_date(transactions, reverse=False)
            elif choose_ascend_descend == 'по убыванию':
                result = sort_by_date(transactions, reverse=True)

        else:
            pass





if __name__ == "__main__":
    main()
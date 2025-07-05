from src.search_and_count import process_bank_search
from src.transaction_reader import read_transactions_from_csv, read_transactions_from_excel
from src.utils import get_transactions
from src.processing import filter_by_state, sort_by_date


def greet_and_choose_file():
    """Шаг 1: Приветствие пользователя и выбор файла."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    while True:
        print("""
        Выберите необходимый пункт меню:
        1. Получить информацию о транзакциях из JSON-файла
        2. Получить информацию о транзакциях из CSV-файла
        3. Получить информацию о транзакциях из XLSX-файла
        """)
        choice = input().strip()

        if choice == '1':
            data = get_transactions(r'src/data/operations.json')
            return 'json', data
        elif choice == '2':
            data = read_transactions_from_csv(r'src/data/transactions.csv')
            return 'csv', data
        elif choice == '3':
            data = read_transactions_from_excel(r'src/data/transactions_excel.xlsx')
            return 'excel', data
        else:
            print(f'Данный пункт меню: {choice} отсутствует')


def filter_by_user_status(data):
    """Шаг 2: Фильтрация по статусу операции."""
    while True:
        print("\nВведите статус, по которому необходимо выполнить фильтрацию:")
        print("Доступные для фильтрации статусы: EXECUTED, CANCELED, PENDING\n")
        status = input().upper()
        if status in ['EXECUTED', 'CANCELED', 'PENDING']:
            filtered_data = filter_by_state(data, state=status)
            # print(filtered_data)
            return filtered_data
        else:
            print(f'Статус операции {status} недоступен.')


def ask_for_sorting(filtered_data):
    """Шаг 3: Предложение пользователю сортировать данные по дате."""
    while True:
        print('\nОтсортировать операции по дате? ')
        answer = input('Да/Нет: ').upper()
        if answer == 'ДА':
            while True:
                print('Отсортировать по возрастанию или по убыванию?')
                order = input('по возрастанию/по убыванию: ').lower()
                if order == 'по возрастанию':
                    sorted_data = sort_by_date(filtered_data, reverse=False)
                    # print(sorted_data)
                    return sorted_data
                elif order == 'по убыванию':
                    sorted_data = sort_by_date(filtered_data, reverse=True)
                    # print(sorted_data)
                    return sorted_data
                else:
                    print('Проверьте корректность ввода')
        elif answer == 'НЕТ':
            return filtered_data
        else:
            print('Проверьте корректность ввода')


def ask_for_description(filtered_data):
    """Шаг 5: Фильтрация по определенному слову в описании."""
    while True:
        print('\nОтфильтровать список транзакций по определенному слову в описании? ')
        answer = input('Да/Нет: ').upper()
        if answer == 'ДА':
            sorted_data = process_bank_search(filtered_data, search=input('Введите слово для поиска транзакций: '))
            # print(sorted_data)
            return sorted_data
        elif answer == 'НЕТ':
            return filtered_data
        else:
            print('Проверьте корректность ввода')


def main():
    """Главная функция, управляющая общей логикой программы."""
    # Шаг 1: Получение данных из файла
    file_type, transactions = greet_and_choose_file()

    # Шаг 2: Фильтрация данных по состоянию
    filtered_data = filter_by_user_status(transactions)

    # Шаг 3: Возможная сортировка по дате
    final_result = ask_for_sorting(filtered_data)

    # Шаг 4: Возможная сортировка по валюте - рубли

    # Шаг 5 Возможный фильтр транзакций по определенному слову в описании
    final_result = ask_for_description(filtered_data)

    print("\nРаспечатываю итоговый список транзакций...")

    print("\nРабота программы завершена.\nРезультат:", final_result)


if __name__ == '__main__':
    main()




# from src.transaction_reader import read_transactions_from_csv, read_transactions_from_excel
# from src.utils import get_transactions
# from src.processing import filter_by_state, sort_by_date
#
#
# def main():
#     """"Функция отвечает за основную логику проекта и связывает функциональности между собой."""
#
#     print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
#     while True:
#         print("""Выберите необходимый пункт меню:
#     1. Получить информацию о транзакциях из JSON-файла
#     2. Получить информацию о транзакциях из CSV-файла
#     3. Получить информацию о транзакциях из XLSX-файла"
#         """)
#         choose_file = input()
#
#         if choose_file == '1':
#             print('Для обработки выбран JSON-файл.')
#             result_json = get_transactions(r'C:\Users\Irina Litvinchuk\PycharmProjects\PythonProject2\src\data\operations.json')
#             #print(result_json)
#             #return result_json
#             break
#
#         elif choose_file == '2':
#             print('Для обработки выбран CSV-файл.')
#             result_csv = read_transactions_from_csv(r'C:\Users\Irina Litvinchuk\PycharmProjects\PythonProject2\src\data\transactions.csv')
#             #print(result_csv)
#             #return result_csv
#             break
#
#
#         elif choose_file == '3':
#             print('Для обработки выбран XLSX-файл.')
#             result_excel = read_transactions_from_excel(r'C:\Users\Irina Litvinchuk\PycharmProjects\PythonProject2\src\data\transactions_excel.xlsx')
#             #print(result_excel)
#             #return result_excel
#             break
#
#         else:
#             print(f'Данный пункт меню: {choose_file} отсутствует')
#             continue
#
#     while True:
#         print("""Введите статус, по которому необходимо выполнить фильтрацию.
# Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING""")
#         choose_status = input().upper()
#         if choose_status in ["EXECUTED", "CANCELED", "PENDING"]:
#             print(f'Операции отфильтрованы по статусу {choose_status}')
#             break
#         else:
#             print(f'Статус операции {choose_status} недоступен.')
#             continue
#
#     if choose_file == '1':
#         result = filter_by_state(result_json, state=f'{choose_status}')
#         print(result)
#     elif choose_file == '2':
#         result = filter_by_state(result_csv, state=f'{choose_status}')
#         print(result)
#
#     elif choose_file == '3':
#         result = filter_by_state(result_excel, state=f'{choose_status}')
#         print(result)
#
#     sort_complete = False
#
#     while not sort_complete:
#         print('Отсортировать операции по дате? ')
#         choose_sort_by_date = input('Да/Нет: ').upper()
#
#         if choose_sort_by_date == 'ДА':
#             while True:  # Вложенный цикл для уточнения порядка сортировки
#                 print('Отсортировать по возрастанию или по убыванию?')
#                 choose_ascend_descend = input('по возрастанию/по убыванию: ').lower()
#
#                 if choose_ascend_descend == 'по возрастанию':
#                     result = sort_by_date(result_json, reverse=False)
#                     print(result)
#                     sort_complete = True  # флаг выхода из обоих циклов
#                     break
#                 elif choose_ascend_descend == 'по убыванию':
#                     result = sort_by_date(result_json, reverse=True)
#                     print(result)
#                     sort_complete = True
#                     break
#                 else:
#                     print('Проверьте корректность ввода')
#
#         elif choose_sort_by_date == 'НЕТ':
#             sort_complete = True  # завершение программы выбором отказа от сортировки
#         else:
#             print('Проверьте корректность ввода')
#
#
#
#
#
# if __name__ == "__main__":
#     main()
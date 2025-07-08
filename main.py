from src.external_api import get_converted_amount
from src.masks import get_mask_card_number, get_mask_account
from src.search_and_count import process_bank_search
from src.transaction_reader import read_transactions_from_csv, read_transactions_from_excel
from src.utils import get_transactions
from src.processing import filter_by_state, sort_by_date
import re


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


def filter_by_status(data):
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
                    filtered_data = sort_by_date(filtered_data, reverse=False)
                    # print(filtered_data)
                    return filtered_data
                elif order == 'по убыванию':
                    filtered_data = sort_by_date(filtered_data, reverse=True)
                    # print(filtered_data)
                    return filtered_data
                else:
                    print('Проверьте корректность ввода')
        elif answer == 'НЕТ':
            return filtered_data
        else:
            print('Проверьте корректность ввода')


def ask_for_rub_convert(filtered_data):
    """Шаг 4: Предложение пользователю конвертировать все операции в рубли"""
    while True:
        print('\nВыводить только рублевые транзакции? ')
        answer = input('Да/Нет: ').upper()
        if answer == 'ДА':
            filtered_data = [
    {
        **transaction,
        'operationAmount': {'amount': converted_amount}
    }
    for transaction in filtered_data
    if (converted_amount := get_converted_amount(transaction)) is not None
]
            # print(filtered_data)
            return filtered_data
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
            filtered_data = process_bank_search(filtered_data, search=input('Введите слово для поиска транзакций: ').lower())
            # print(sorted_data)
            return filtered_data
        elif answer == 'НЕТ':
            return filtered_data
        else:
            print('Проверьте корректность ввода')


def display_transactions(filtered_data):
    """Функция для красивого вывода операций в консоль."""
    print("\nРаспечатываю итоговый список транзакций...")
    if not filtered_data:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    # Заголовок таблицы
    print(f"{'Программа:'}\nВсего банковских операций в выборке: {len(filtered_data)}\n")

    # Шаблон для каждой транзакции
    for idx, transaction in enumerate(filtered_data):
        date = transaction.get('date', '')[:10]
        description = transaction.get('description', '')
        amount = transaction.get('operationAmount', {}).get('amount', '')
        currency = transaction.get('operationAmount', {}).get('currency', {}).get('code', '')

        frm = transaction.get('from', '')
        to = transaction.get('to', '')

        # Применяем регулярные выражения для маскировки номеров
        def apply_masks(text):
            text = str(text)
            text = re.sub(r'\b\d{16}\b', lambda x: get_mask_card_number(x.group()), text)
            text = re.sub(r'\b\d{20}\b', lambda x: get_mask_account(x.group()), text)
            return text

        # Обрабатываем обе стороны операции
        frm_masked = apply_masks(frm)
        to_masked = apply_masks(to)

        # Формируем детальную запись транзакции
        operation_details = f"{date} {description}\n"
        if frm and to:
            operation_details += f"{frm_masked} -> {to_masked}\n"
        elif frm:
            operation_details += f"{frm_masked}\n"
        elif to:
            operation_details += f"{to_masked}\n"
        operation_details += f"Сумма: {amount} {currency}\n\n"

        print(operation_details)


def main():
    """"Функция отвечает за основную логику проекта и связывает функциональности между собой."""
    # Шаг 1: Получение данных из файла
    file_type, transactions = greet_and_choose_file()

    # Шаг 2: Фильтрация данных по статусу операции
    filtered_data = filter_by_status(transactions)

    # Шаг 3: Возможная сортировка по дате
    result = ask_for_sorting(filtered_data)

    # Шаг 4: Возможная сортировка по валюте - рубли
    result = ask_for_rub_convert(result)

    # Шаг 5 Возможный фильтр транзакций по определенному слову в описании
    result = ask_for_description(result)

    # Шаг 6 Распечатываем результат
    result = display_transactions(result)


if __name__ == '__main__':
    main()

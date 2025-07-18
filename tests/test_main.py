from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

import pytest

import main
from main import (ask_for_description, ask_for_rub_convert, ask_for_sorting, display_transactions, filter_by_status,
                  greet_and_choose_file, normalize_transaction)


def test_greet_and_choose_file_json():
    """Заменяем input с выбором JSON-файла"""
    with patch("builtins.input", side_effect=["1"]):
        result = greet_and_choose_file()
        assert result[0] == "json"


def test_greet_and_choose_file_csv():
    """Заменяем input с выбором CSV-файла"""
    with patch("builtins.input", side_effect=["2"]):
        result = greet_and_choose_file()
        assert result[0] == "csv"


def test_greet_and_choose_file_excel():
    """Заменяем input с выбором Excel-файла"""
    with patch("builtins.input", side_effect=["3"]):
        result = greet_and_choose_file()
        assert result[0] == "excel"


def test_greet_and_choose_file_invalid_option(capsys):
    """Симулируем ввод несуществующего пункта меню"""
    with patch("builtins.input", side_effect=["4", "4", "4"]):
        result = greet_and_choose_file()
        assert result == (None, None)  # функция возвращает None при превышении попыток

    # Только после выполнения функции вызываем capsys
    captured = capsys.readouterr()
    assert "Данный пункт меню: 4 отсутствует" in captured.out


def test_filter_by_status():
    """Тестирование функции фильтрации по статусу с фиктивным вводом пользователя"""
    mock_data = [{"state": "EXECUTED"}, {"state": "CANCELED"}, {"state": "PENDING"}]

    # Заменяем input() на фиктивное значение "EXECUTED"
    with patch("builtins.input", return_value="EXECUTED"):
        result = filter_by_status(mock_data)
        assert len(result) > 0
        assert all(txn["state"] == "EXECUTED" for txn in result)

    # Проверим другой статус, например "CANCELED"
    with patch("builtins.input", return_value="CANCELED"):
        result = filter_by_status(mock_data)
        assert len(result) > 0
        assert all(txn["state"] == "CANCELED" for txn in result)


def test_filter_by_status_invalid():
    """Проверка поведения при некорректном вводе статуса"""
    mock_data = [{"state": "EXECUTED"}, {"state": "CANCELED"}, {"state": "PENDING"}]

    # Симулируем ввод неправильного статуса
    with patch("builtins.input", return_value="UNKNOWN"):
        result = filter_by_status(mock_data)
        assert result is None  # ожидаем, что функция вернет None при превышении попыток


test_data = [{"date": "2023-08-15"}, {"date": "2023-07-20"}, {"date": "2023-09-01"}]


def run_test_ask_for_sorting(input_values, expected_output):
    """Проверка запроса на сортировку при разном вводе пользователя"""
    with patch("builtins.input", side_effect=input_values):
        result = ask_for_sorting(test_data.copy())
        assert result == expected_output, f"Expected output: {expected_output}, but got: {result}"


def test_sort_ascending():
    """Пользователь согласился на сортировку по возрастанию"""
    input_values = ["ДА", "по возрастанию"]
    expected_output = sorted(test_data, key=lambda x: x["date"])
    run_test_ask_for_sorting(input_values, expected_output)


def test_sort_descending():
    """Пользователь согласился на сортировку по убыванию"""
    input_values = ["ДА", "по убыванию"]
    expected_output = sorted(test_data, key=lambda x: x["date"], reverse=True)
    run_test_ask_for_sorting(input_values, expected_output)


def test_no_sorting():
    """Пользователь отказался от сортировки"""
    input_values = ["НЕТ"]
    expected_output = test_data
    run_test_ask_for_sorting(input_values, expected_output)


def test_incorrect_answer_then_correct():
    """Проверка обработки неправильного ввода пользователя, затем правильного"""
    input_values = ["НЕПРАВИЛЬНЫЙ_ОТВЕТ", "ДА", "по возрастанию"]
    expected_output = sorted(test_data, key=lambda x: x["date"])
    run_test_ask_for_sorting(input_values, expected_output)


def test_max_attempt_reached():
    """Проверка завершения работы при исчерпании количества попыток"""
    input_values = ["ПЛОХОЙ_ОТВЕТ"] * 3
    expected_output = None
    run_test_ask_for_sorting(input_values, expected_output)


# if __name__ == "__main__":
#     try:
#         test_sort_ascending()
#         test_sort_descending()
#         test_no_sorting()
#         test_incorrect_answer_then_correct()
#         test_max_attempt_reached()
#         print("Все тесты пройдены успешно!")
#     except AssertionError as e:
#         print(e)


# Тестируем случай, когда пользователь выбирает конвертацию
@patch("main.get_converted_amount")  # Патчим по месту ИМПОРТА
def test_ask_for_rub_convert_yes(mock_get_converted_amount):
    transactions = [
        {"operationAmount": {"amount": "100", "currency": {"code": "USD"}}},
        {"operationAmount": {"amount": "200", "currency": {"code": "EUR"}}},
        {"operationAmount": {"amount": "300", "currency": {"code": "RUB"}}},
    ]

    mock_get_converted_amount.side_effect = [7800.0, 16000.0, 300.0]

    expected_result = [
        {"operationAmount": {"amount": 7800.0}},
        {"operationAmount": {"amount": 16000.0}},
        {"operationAmount": {"amount": 300.0}},
    ]

    with patch("builtins.input", return_value="ДА"):
        result = ask_for_rub_convert(transactions, use_mock=True)

    assert result == expected_result


@patch("main.get_converted_amount")
def test_ask_for_rub_convert_no(mock_get_converted_amount):
    transactions = [
        {"operationAmount": {"amount": "100", "currency": {"code": "USD"}}},
        {"operationAmount": {"amount": "200", "currency": {"code": "EUR"}}},
        {"operationAmount": {"amount": "300", "currency": {"code": "RUB"}}},
    ]

    with patch("builtins.input", return_value="НЕТ"):
        result = ask_for_rub_convert(transactions, use_mock=True)

    assert result == transactions
    mock_get_converted_amount.assert_not_called()  # Убедимся, что внешний API не использовался


def test_ask_for_rub_convert_incorrect_input():
    """Проверка обработки неправильного ввода пользователя."""
    transactions = []

    # Три раза введён неправильный ввод ("ABC"), потом правильный ("ДА")
    with (
        patch("builtins.input", side_effect=["ABC", "ABC", "ABC", "ДА"]),
        patch("main.get_converted_amount"),
    ):
        result = ask_for_rub_convert(transactions, use_mock=True)
        assert result is None  # Так как никакие транзакции не были обработаны из-за ограничений по попыткам


def test_ask_for_rub_convert_max_attempt_reached():
    """Проверка завершения работы функции когда попытки превышены."""
    transactions = []

    # Неправильный ввод четыре раза подряд
    with (
        patch("builtins.input", side_effect=["ABC", "ABC", "ABC", "ABC"]),
        patch("main.get_converted_amount"),
    ):
        result = ask_for_rub_convert(transactions, use_mock=True)
        assert result is None  # Возвращается None при превышении количества попыток


def test_ask_for_description_yes():
    """Проверка подтверждения фильтрации с указанием конкретного слова."""
    transactions = [
        {"description": "Оплата услуг"},
        {"description": "Покупка продуктов"},
        {"description": "Перевод другу"},
    ]

    # Эмулируем ввод пользователя
    user_inputs = iter(["ДА", "перевод"])

    with patch("builtins.input", lambda _: next(user_inputs)):
        result = ask_for_description(transactions)

    expected_filtered_data = [{"description": "Перевод другу"}]
    assert result == expected_filtered_data


def test_ask_for_description_no():
    """Проверка отказа от фильтрации."""
    transactions = [{"description": "Оплата налогов"}, {"description": "Оплата кредита"}]

    # Эмулируем ввод пользователя
    with patch("builtins.input", return_value="НЕТ"):
        result = ask_for_description(transactions)

    # Список должен вернуться без изменений
    assert result == transactions


def test_ask_for_description_too_many_attempts():
    """Проверка окончания работы при множестве неверных ответов."""
    transactions = [{"description": "Оплата ЖКХ"}]

    # Эмулируем серию неправильных ответов
    user_inputs = iter(["abc", "123", "xyz"])

    with patch("builtins.input", lambda _: next(user_inputs)), patch("builtins.print") as mocked_print:
        result = ask_for_description(transactions)

    # Функция должна возвратить None при превышении попыток
    assert result is None, "Возвращаемое значение отличается от ожидаемого."
    mocked_print.assert_any_call("Максимальное число попыток достигнуто. Завершаем работу.")


def test_normalize_valid_json_transaction():
    """Нормализация JSON-транзакции"""
    json_transaction = {
        "id": "12345",
        "state": "EXECUTED",
        "date": "2023-01-01T12:00:00Z",
        "operationAmount": {"amount": "1000", "currency": {"name": "RUB", "code": "643"}},
        "from": "Card number 123456******1234",
        "to": "Account number 123456******1234",
        "description": "Test Transaction",
    }

    expected_output = {
        "id": 12345,
        "state": "EXECUTED",
        "date": "2023-01-01T12:00:00Z",
        "amount": "1000",
        "currency": {"name": "RUB", "code": "643"},
        "from": "Card number 123456******1234",
        "to": "Account number 123456******1234",
        "description": "Test Transaction",
    }

    actual_result = normalize_transaction(json_transaction)
    assert actual_result == expected_output, f"Результат {actual_result} не совпадает с ожидаемым {expected_output}"


def test_normalize_valid_csv_transaction():
    """Нормализация CSV-транзакции"""
    csv_transaction = {
        "id": "67890",
        "state": "CANCELED",
        "date": "2023-01-02T13:00:00Z",
        "amount": "2000",
        "currency_name": "USD",
        "currency_code": "840",
        "from": "",
        "to": "Account number 987654******1234",
        "description": "Canceled Transaction",
    }

    expected_output = {
        "id": 67890,
        "state": "CANCELED",
        "date": "2023-01-02T13:00:00Z",
        "amount": "2000",
        "currency": {"name": "USD", "code": "840"},
        "from": "",
        "to": "Account number 987654******1234",
        "description": "Canceled Transaction",
    }

    actual_result = normalize_transaction(csv_transaction)
    assert actual_result == expected_output, f"Результат {actual_result} не совпадает с ожидаемым {expected_output}"


def test_normalize_missing_values():
    """Нормализация транзакции с пропущенными полями"""
    incomplete_transaction = {"id": "12345", "state": "EXECUTED", "date": "2023-01-01T12:00:00Z", "from": ""}

    expected_output = {
        "id": 12345,
        "state": "EXECUTED",
        "date": "2023-01-01T12:00:00Z",
        "amount": "",
        "currency": {"name": "", "code": ""},
        "from": "",
        "to": "",
        "description": "",
    }

    actual_result = normalize_transaction(incomplete_transaction)
    assert actual_result == expected_output, f"Результат {actual_result} не совпадает с ожидаемым {expected_output}"


def test_normalize_invalid_input():
    """ "Неправильные данные (не словарь)"""
    invalid_transaction = "Not a dictionary"
    with pytest.raises(TypeError, match="Входные данные должны быть словарем"):
        normalize_transaction(invalid_transaction)


# Подготовим данные для тестов display_transactions
transactions = [
    {
        "id": "12345",
        "state": "EXECUTED",
        "date": "2023-01-01T12:00:00Z",
        "operationAmount": {"amount": "1000", "currency": {"name": "RUB", "code": "643"}},
        "from": "Card number 123456******1234",
        "to": "Account number 123456******1234",
        "description": "Перевод с карты на счет",
    },
    {
        "id": "67890",
        "state": "CANCELED",
        "date": "2023-01-02T13:00:00Z",
        "operationAmount": {"amount": "2000", "currency": {"name": "USD", "code": "840"}},
        "from": "",
        "to": "Account number 987654******1234",
        "description": "Перевод организации",
    },
]

partial_transactions = [
    {
        "id": "12345",
        "state": "EXECUTED",
        "date": "2023-01-01T12:00:00Z",
        "operationAmount": {"amount": "1000", "currency": {"name": "RUB", "code": "643"}},
    },
    {
        "id": "67890",
        "state": "CANCELED",
        "date": "2023-01-02T13:00:00Z",
        "operationAmount": {"amount": "2000", "currency": {"name": "USD", "code": "840"}},
        "description": "",
    },
]


def test_display_transactions_valid_data():
    """Проверка вывода транзакций при наличии данных"""
    with redirect_stdout(StringIO()) as out:
        display_transactions(transactions)
    output = out.getvalue()
    assert "Распечатываю итоговый список транзакций..." in output
    assert "Всего банковских операций в выборке: 2" in output
    assert "Сумма: 1000 643" in output
    assert "Сумма: 2000 840" in output


def test_display_transactions_no_data():
    """Проверка реакции на отсутствие данных"""
    with redirect_stdout(StringIO()) as out:
        display_transactions([])
    output = out.getvalue()
    assert "Не найдено ни одной транзакции, подходящей под ваши условия фильтрации." in output


def test_display_transactions_partial_data():
    """Проверка обработки транзакций с недостающими полями"""
    with redirect_stdout(StringIO()) as out:
        display_transactions(partial_transactions)
    output = out.getvalue()
    assert "Распечатываю итоговый список транзакций..." in output
    assert "Всего банковских операций в выборке: 2" in output
    assert "Сумма: 1000 643" in output
    assert "Сумма: 2000 840" in output


def test_display_transactions_wrong_type():
    """Неправильный тип данных (не словарь)"""
    wrong_data = "This is not a dictionary"
    with pytest.raises(TypeError, match="Входные данные должны быть словарем"):
        display_transactions(wrong_data)


# Фиктивные транзакции для теста main()
fake_transactions = [
    {
        "id": "12345",
        "state": "EXECUTED",
        "date": "2023-01-01T12:00:00Z",
        "operationAmount": {"amount": "1000", "currency": {"name": "RUB", "code": "643"}},
        "from": "Card number 123456******1234",
        "to": "Account number 123456******1234",
        "description": "Test Transaction",
    },
    {
        "id": "67890",
        "state": "CANCELED",
        "date": "2023-01-02T13:00:00Z",
        "operationAmount": {"amount": "2000", "currency": {"name": "USD", "code": "840"}},
        "from": "",
        "to": "Account number 987654******1234",
        "description": "Canceled Transaction",
    },
]


# Основной тест
@patch("main.get_transactions", return_value=fake_transactions)
@patch("main.display_transactions")
def test_main_function(mock_display, mock_get_transactions):
    """Основной тест: пользователь вводит"""
    # Моделируем пользовательский ввод
    inputs = [
        "1",  # выбор JSON
        "EXECUTED",  # фильтрация по статусу
        "Да",  # сортировать по дате
        "по возрастанию",  # направление сортировки
        "Нет",  # не конвертировать в рубли
        "Да",  # фильтровать по описанию
        "Test",  # фильтр по описанию
    ]

    with patch("builtins.input", side_effect=inputs):
        main.main(use_mock=True)

    # Проверяем, что транзакции были получены
    mock_get_transactions.assert_called_once()
    # Проверяем, что результат был выведен
    mock_display.assert_called_once()


@patch("main.get_transactions")
def test_main_function_bad_choice(mock_get_transactions, capsys):
    """Тестирование неправильного ввода 3 раза подряд и завершения программы"""
    bad_inputs = ["4", "4", "4"]

    with patch("builtins.input", side_effect=bad_inputs):
        main.main(use_mock=True)

    captured = capsys.readouterr()
    output = captured.out

    # Проверяем, что трижды вывелась ошибка
    assert output.count("Данный пункт меню: 4 отсутствует") == 3
    assert "Максимальное число попыток достигнуто" in output
    assert mock_get_transactions.call_count == 0

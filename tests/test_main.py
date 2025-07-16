import pytest
from unittest.mock import patch, Mock
from main import (
    greet_and_choose_file,
    filter_by_status,
    ask_for_sorting,
    ask_for_rub_convert,
    ask_for_description,
    normalize_transaction,
)

from src.external_api import get_converted_amount
import src.external_api
import requests


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
    # Подготавливаем тестовые данные
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
    mock_data = [{"state": "EXECUTED"}, {"state": "CANCELED"}, {"state": "PENDING"}]

    # Симулируем ввод неправильного статуса
    with patch("builtins.input", return_value="UNKNOWN"):
        result = filter_by_status(mock_data)
        assert result is None  # ожидаем, что функция вернет None при превышении попыток


test_data = [{"date": "2023-08-15"}, {"date": "2023-07-20"}, {"date": "2023-09-01"}]


def run_test_ask_for_sorting(input_values, expected_output):
    with patch("builtins.input", side_effect=input_values):
        result = ask_for_sorting(test_data.copy())
        assert result == expected_output, f"Expected output: {expected_output}, but got: {result}"


def test_sort_ascending():
    input_values = ["ДА", "по возрастанию"]
    expected_output = sorted(test_data, key=lambda x: x["date"])
    run_test_ask_for_sorting(input_values, expected_output)


def test_sort_descending():
    input_values = ["ДА", "по убыванию"]
    expected_output = sorted(test_data, key=lambda x: x["date"], reverse=True)
    run_test_ask_for_sorting(input_values, expected_output)


def test_no_sorting():
    input_values = ["НЕТ"]
    expected_output = test_data
    run_test_ask_for_sorting(input_values, expected_output)


def test_incorrect_answer_then_correct():
    input_values = ["НЕПРАВИЛЬНЫЙ_ОТВЕТ", "ДА", "по возрастанию"]
    expected_output = sorted(test_data, key=lambda x: x["date"])
    run_test_ask_for_sorting(input_values, expected_output)


def test_max_attempt_reached():
    input_values = ["ПЛОХОЙ_ОТВЕТ"] * 3
    expected_output = None
    run_test_ask_for_sorting(input_values, expected_output)


if __name__ == "__main__":
    try:
        test_sort_ascending()
        test_sort_descending()
        test_no_sorting()
        test_incorrect_answer_then_correct()
        test_max_attempt_reached()
        print("Все тесты пройдены успешно!")
    except AssertionError as e:
        print(e)


# # Тестируем случай, когда пользователь выбирает конвертацию
# @patch("src.external_api.get_converted_amount")
# @patch("requests.request", new_callable=lambda: Mock(return_value=Mock(status_code=200, json=lambda: {"result": 1000.0})))
# def test_ask_for_rub_convert_yes(mock_request, mock_get_converted_amount):
#     """Проверка работы функции при выборе 'Да' на предложение конвертировать транзакции."""
#     transactions = [
#         {"operationAmount": {"amount": "100", "currency": {"code": "USD"}}},
#         {"operationAmount": {"amount": "200", "currency": {"code": "EUR"}}},
#         {"operationAmount": {"amount": "300", "currency": {"code": "RUB"}}},  # Валюта уже в рублях
#     ]
#
#     # Эмулируем успешную конвертацию
#     mock_get_converted_amount.side_effect = [7800.0, 16000.0, 300.0]
#
#     # Получаемый результат
#     expected_result = [
#         {"operationAmount": {"amount": 7800.0}},
#         {"operationAmount": {"amount": 16000.0}},
#         {"operationAmount": {"amount": 300.0}}
#     ]
#
#     # Маска для печати и запросов
#     with patch('builtins.print'), patch('requests.request'):
#         # Предоставляем ответ пользователя вручную ('ДА')
#         with patch('builtins.input', side_effect=['ДА']):
#             result = ask_for_rub_convert(transactions)
#
#     # Проверяем результат
#     assert result == expected_result, "Полученные данные отличаются от ожидаемого результата."
#
#     # Проверяем, что реальные запросы не осуществились
#     mock_request.assert_not_called()


# Тестируем случай отказа от конвертации
def test_ask_for_rub_convert_no():
    """Проверка работы функции при отказе от конвертации транзакций."""
    transactions = [
        {"operationAmount": {"amount": "100", "currency": {"code": "USD"}}},
        {"operationAmount": {"amount": "200", "currency": {"code": "EUR"}}},
        {"operationAmount": {"amount": "300", "currency": {"code": "RUB"}}},
    ]

    # Пользователь отказался от конвертации
    with (
        patch("builtins.input", side_effect=["НЕТ"]),
        patch("src.external_api.get_converted_amount") as mock_get_converted_amount,
    ):
        result = ask_for_rub_convert(transactions)
        assert result == transactions
        mock_get_converted_amount.assert_not_called()  # Убедимся, что внешний API не использовался


# Тестируем обработку неверного ввода
def test_ask_for_rub_convert_incorrect_input():
    """Проверка обработки неправильного ввода пользователя."""
    transactions = []

    # Три раза введён неправильный ввод ("ABC"), потом правильный ("ДА")
    with (
        patch("builtins.input", side_effect=["ABC", "ABC", "ABC", "ДА"]),
        patch("src.external_api.get_converted_amount"),
    ):
        result = ask_for_rub_convert(transactions)
        assert result is None  # Так как никакие транзакции не были обработаны из-за ограничений по попыткам


# Тестируем ситуацию, когда попытки превышены
def test_ask_for_rub_convert_max_attempt_reached():
    """Проверка завершения работы функции при исчерпании числа попыток."""
    transactions = []

    # Неправильный ввод четыре раза подряд
    with (
        patch("builtins.input", side_effect=["ABC", "ABC", "ABC", "ABC"]),
        patch("src.external_api.get_converted_amount"),
    ):
        result = ask_for_rub_convert(transactions)
        assert result is None  # Возвращается None при превышении количества попыток


# Тест №1: Пользователь подтверждает фильтрацию и вводит слово для поиска
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

    # Предположим, что фильтр нашел одну транзакцию
    expected_filtered_data = [{"description": "Перевод другу"}]
    assert result == expected_filtered_data


# Тест №2: Пользователь отклоняет фильтрацию
def test_ask_for_description_no():
    """Проверка отклонения фильтрации."""
    transactions = [{"description": "Оплата налогов"}, {"description": "Оплата кредита"}]

    # Эмулируем ввод пользователя
    with patch("builtins.input", return_value="НЕТ"):
        result = ask_for_description(transactions)

    # Список должен вернуться без изменений
    assert result == transactions


# Тест №3: Пользователь делает много неверных вводов
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


# Тест 1: Нормализация JSON-транзакции
def test_normalize_valid_json_transaction():
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


# Тест 2: Нормализация CSV-транзакции
def test_normalize_valid_csv_transaction():
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


# Тест 3: Нормализация транзакции с пропущенными полями
def test_normalize_missing_values():
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


# Тест 4: Неправильные данные (не словарь)
def test_normalize_invalid_input():
    invalid_transaction = "Not a dictionary"
    with pytest.raises(TypeError, match="Входные данные должны быть словарем"):
        normalize_transaction(invalid_transaction)

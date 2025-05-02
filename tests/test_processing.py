import pytest

from src.processing import filter_by_state, sort_by_date


def test_filter_by_state(transactions: list) -> None:
    """Тестирование фильтрации списка словарей по заданному статусу state (по умолчанию=EXECUTED)"""
    assert filter_by_state(transactions) == [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]


def test_filter_by_state_no_state() -> None:
    """Проверка работы функции при отсутствии словарей с указанным статусом state в списке"""
    assert (
        filter_by_state(
            [
                {"id": 41428829, "state": "", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "", "date": "2018-10-14T08:21:33.419441"},
            ]
        )
        == "Статус операции отсутствует. Проверьте данные"
    )


@pytest.mark.parametrize(
    "state, expected",
    [
        (
            "EXECUTED",
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
        ),
        (
            "CANCELED",
            [
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
        ),
    ],
)
def test_filter_by_state_different_state(transactions: list, state: str, expected: list) -> None:
    """Параметризация тестов для различных возможных значений статуса state"""
    assert filter_by_state(transactions, state) == expected


def test_sort_by_date_descending(transactions: list) -> None:
    """Тестирование сортировки списка словарей по датам в порядке убывания"""
    assert sort_by_date(transactions) == [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]


def test_sort_by_date_ascending(transactions: list) -> None:
    """Тестирование сортировки списка словарей по датам в порядке возрастания"""
    assert sort_by_date(transactions, False) == [
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    ]


def test_sort_by_date_same_date_diff_time() -> None:
    """Проверка корректности сортировки при одинаковых датах, функция сортирует по времени"""
    assert sort_by_date(
        [
            {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            {"id": 939719570, "state": "EXECUTED", "date": "2019-07-03T02:08:58.425572"},
            {"id": 594226727, "state": "CANCELED", "date": "2019-07-03T21:27:25.241689"},
            {"id": 615064591, "state": "CANCELED", "date": "2019-07-03T08:21:33.419441"},
        ]
    ) == [
        {"id": 594226727, "state": "CANCELED", "date": "2019-07-03T21:27:25.241689"},
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 615064591, "state": "CANCELED", "date": "2019-07-03T08:21:33.419441"},
        {"id": 939719570, "state": "EXECUTED", "date": "2019-07-03T02:08:58.425572"},
    ]


def test_sort_by_date_same_date(transactions_same_dates: list) -> None:
    """Проверка корректности обработки ошибки сортировки при одинаковых датах"""
    with pytest.raises(ValueError) as exc_info:
        sort_by_date(transactions_same_dates)

    assert str(exc_info.value) == "Проверьте корректность даты операции: найдены повторяющиеся даты."


def test_sort_by_date_invalid_input() -> None:
    """Тест проверки поведения функции при передаче некорректных данных"""
    with pytest.raises(ValueError) as exc_info:
        sort_by_date(
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "invalid-date"},  # Некорректная дата
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ]
        )
    assert str(exc_info.value) == "Некорректно указан формат входных данных"

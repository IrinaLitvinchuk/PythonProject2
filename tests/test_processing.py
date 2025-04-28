from idlelib.pyparse import trans

import pytest
from src.processing import filter_by_state
from tests.conftest import transactions


def test_filter_by_state(transactions) -> None:
    """Тестирование фильтрации списка словарей по заданному статусу state (по умолчанию=EXECUTED)"""
    assert filter_by_state(transactions) == [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]


def test_filter_by_state_no_state() -> None:
    """Проверка работы функции при отсутствии словарей с указанным статусом state в списке"""
    assert filter_by_state([{"id": 41428829, "state": "", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "", "date": "2018-10-14T08:21:33.419441"},]) == "Статус операции отсутствует. Проверьте данные"


@pytest.mark.parametrize("transactions, state, expected",
                         [
                             (transactions, "EXECUTED",  [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},],)])

def test_filter_by_state_different_state(transactions, state, expected) -> None:
    assert filter_by_state([
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
], state) == expected
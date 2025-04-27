import pytest
from src.masks import get_mask_card_number
from src.masks import get_mask_account

def test_get_mask_card_number(card_number):
    assert get_mask_card_number(card_number) == '7000 79** **** 6361'


def test_get_mask_card_number_empty():
    assert get_mask_card_number('') == 'Введите номер карты'


def test_get_mask_card_number_wrong_digits():
    assert get_mask_card_number("12345") == 'Номер карты должен состоять из 16 цифр'


def test_get_mask_card_number_wrong_type():
    with pytest.raises(TypeError):
        get_mask_card_number(12345)

def test_get_mask_account(account_number):
    assert get_mask_account(account_number) == '**4305'

def test_get_mask_account_wrong_type():
    with pytest.raises(TypeError):
        get_mask_account(12345)


def test_get_mask_account_wrong_digit_count():
    assert get_mask_account('12345') == 'Номер счета должен состоять из 20 цифр'


def test_get_mask_account_empty():
    assert get_mask_account('') == 'Ведите номер счета'

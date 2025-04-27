import pytest
from src.masks import get_mask_card_number

def test_get_mask_card_number(card_number):
    assert get_mask_card_number(card_number) == '7000 79** **** 6361'


def test_get_mask_card_number_empty():
    assert get_mask_card_number('') == 'Введите номер карты. Номер карты состоит из 16 цифр'

def test_get_mask_card_number_wrong_digits():
    assert get_mask_card_number("12345") == 'Введите номер карты. Номер карты состоит из 16 цифр'


def test_get_mask_card_number_wrong_type():
    with pytest.raises (TypeError):
        get_mask_card_number(12345)







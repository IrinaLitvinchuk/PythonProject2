from calendar import month

from src.masks import get_mask_card_number
from src.masks import get_mask_account


def mask_account_card(account_or_card_number: str) -> str:
    """Функция, маскирующая номер карты или счета"""
    new_mask = []
    split_input = account_or_card_number.split()
    number = split_input[-1]
    if len(number) == 16 or len(number) == 20:
        for element in split_input:
            if element.isalpha():
                new_mask.append(element)
            else:
                if len(number) == 16:
                    card_number = get_mask_card_number(number)
                    new_mask.append(card_number)
                else:
                    account_number = get_mask_account(number)
                    new_mask.append(account_number)
    else:
        print("Введен некорректный номер карты или счета")

    return " ".join(new_mask)


account_or_card_number = input("Введите данные карты или счета: ")
print(mask_account_card(account_or_card_number))


def get_date(date_input: str) -> str:
    """Функция принимает на вход строку и отдает корректный результат в формате 11.07.2018"""

    # первый вариант
    # day = date_input[8:10]
    # month = date_input[5:7]
    # year = date_input[:4]
    # new_date = day + "." + month + "." + year

    # второй вариант лучше (сама не додумалась)
    new_date_list = date_input[:10].split("-")[::-1]
    new_date = ".".join(new_date_list)

    return new_date


print(get_date("2024-03-11T02:26:18.671407"))

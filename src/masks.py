from mypy.checkexpr import replace_callable_return_type


def get_mask_card_number(card_number: str) -> str:
    """Функция, которая принимает на вход номер карты и возвращает ее маску"""
    if card_number != "":
        if isinstance(card_number, str):
            if len(card_number) == 16:
                return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
            return "Номер карты должен состоять из 16 цифр"
        else:
            raise TypeError
    return "Введите номер карты"


def get_mask_account(account_number: str) -> str:
    """Функция, которая принимает на вход номер счета и возвращает его маску"""
    if account_number != "":
        if isinstance(account_number, str):
            if len(account_number) == 20:
                return f"**{account_number[-4:]}"
            return "Номер счета должен состоять из 20 цифр"
        else:
            raise TypeError
    return "Ведите номер счета"

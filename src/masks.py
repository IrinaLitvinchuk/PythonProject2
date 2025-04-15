def get_mask_card_number(card_number: str) -> str:
    """Функция, которая принимает на вход номер карты и возвращает ее маску"""
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


card_number = input("Номер карты: ")
print(get_mask_card_number(card_number))


def get_mask_account(account_number: str) -> str:
    """Функция, которая принимает на вход номер счета и возвращает его маску"""
    return f"**{account_number[-4:]}"


account_number = input("Номер счета: ")
print(get_mask_account(account_number))

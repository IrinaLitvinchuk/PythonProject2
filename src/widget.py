def mask_account_card(account_or_card_number: str) -> str:
    """Функция, маскирующая номер карты или счета"""
    from src.masks import get_mask_card_number
    from src.masks import get_mask_account

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

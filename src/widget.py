from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_or_card_number: str) -> str:
    """Функция, маскирующая номер карты или счета"""
    if isinstance(account_or_card_number, str):
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
            return """Введен некорректный номер карты или счета.
            Номер карты состоит из 16 цифр.
            Номер счета состоит из 20 цифр"""

        return " ".join(new_mask)
    raise TypeError


def get_date(date_input: str) -> str:
    """Функция принимает на вход строку и отдает корректный результат в формате 11.07.2018"""
    if date_input == "":
        return "Отсутствует дата. Проверьте корректность входных данных"
    else:
        if isinstance(date_input, str):
            new_date_list = date_input[:10].split("-")[::-1]
            new_date = ".".join(new_date_list)
            return new_date
        else:
            raise TypeError

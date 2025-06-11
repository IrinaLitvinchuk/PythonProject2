import logging

masks_logger = logging.getLogger('masks_logger')
file_handler = logging.FileHandler('../logs/masks.log', mode="w", encoding='utf-8')
file_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
masks_logger.addHandler(file_handler)
masks_logger.setLevel(logging.DEBUG)


def get_mask_card_number(card_number: str) -> str:
    """Функция, которая принимает на вход номер карты и возвращает ее маску"""
    masks_logger.info(f'Номер карты для маскировки {card_number}')
    if card_number != "":
        if isinstance(card_number, str):
            if len(card_number) == 16:
                masked_card_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
                masks_logger.info(f'Получен замаскированный номер карты {masked_card_number}')
                return masked_card_number
            masks_logger.error('Номер карты должен состоять из 16 цифр')
            return "Номер карты должен состоять из 16 цифр"
        else:
            masks_logger.error('Проверьте тип данных. Номер должен состоять из цифр')
            raise TypeError
    masks_logger.error('Пустая строка. Введите номер карты')
    return "Введите номер карты"


def get_mask_account(account_number: str) -> str:
    """Функция, которая принимает на вход номер счета и возвращает его маску"""
    masks_logger.info(f'Номер счета для маскировки {account_number}')
    if account_number != "":
        if isinstance(account_number, str):
            if len(account_number) == 20:
                masked_account_number = f"**{account_number[-4:]}"
                masks_logger.info(f'Получен замаскированный номер счета {masked_account_number}')
                return masked_account_number
            masks_logger.error('Номер счета должен состоять из 20 цифр')
            return "Номер счета должен состоять из 20 цифр"
        else:
            masks_logger.error('Проверьте тип данных. Номер должен состоять из цифр')
            raise TypeError
    masks_logger.error('Пустая строка. Ведите номер счета')
    return "Ведите номер счета"

#print(get_mask_card_number('7000792289606361'))
#print(get_mask_card_number('700079228960636'))
#print(get_mask_card_number(''))

print(get_mask_account('73654108430135874305'))
print(get_mask_account('736541084301358743'))
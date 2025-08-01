# Проект "Виджет для банковского приложения"

## Описание:

Проект "Виджет для банковского приложения" - это новый функционал на Python для личного кабинета клиента банка.  
Это виджет, который показывает несколько последних успешных банковских операций клиента.

**Проект содержит ряд полезных функций:**
* Функции маскировки номера банковской карты `get_mask_card_number` и номера банковского счета `get_mask_account`
* Функцию `mask_account_card`, которая умеет обрабатывать информацию как о картах, так и о счетах
* Функцию для преобразования даты `get_date` ("2024-03-11T02:26:18.671407" -> "11.03.2024")
* Функцию `filter_by_state`, которая фильтрует список операций по значению ключа 'state' (по умолчанию "EXECUTED")
* Функцию `sort_by_date`, которая сортирует список операций по убыванию, т.е. сначала самые последние операции

## Установка:

1. Клонируйте репозиторий:
```
git clone https://github.com/IrinaLitvinchuk/PythonProject2.git
```
2. Установите зависимости:
```
poetry install
```

## Примеры работы функций:

1. Функция `get_mask_card_number` принимает на вход номер карты и возвращает ее маску формате XXXX XX** **** XXXX, где X — это цифра номера.
   ```
   7000792289606361     # входной аргумент
   7000 79** **** 6361  # выход функции
   ```
2. Функция `get_mask_account` принимает на вход номер счета и возвращает его маску  в формате **XXXX, где X — это цифра номера.
   ```
   73654108430135874305  # входной аргумент
   **4305  # выход функции
   ```
3. Функция `mask_account_card` принимает строку, содержащую тип и номер карты или счета и возвращает строку с замаскированным номером.
   ```
   # Пример для карты
   Visa Platinum 7000792289606361  # входной аргумент
   Visa Platinum 7000 79** **** 6361  # выход функции
   
   # Пример для счета
   Счет 73654108430135874305  # входной аргумент
   Счет **4305  # выход функции
   ```
4. Функция `get_date` принимает на вход строку с датой в формате `"2024-03-11T02:26:18.671407"` и возвращает строку с датой в формате
`"ДД.ММ.ГГГГ" ("11.03.2024").`

5. Функция `filter_by_state` принимает список словарей и опционально значение для ключа `'state'` (по умолчанию `'EXECUTED'`),
   и возвращает новый список словарей, содержащий только те словари, у которых ключ соответствует указанному значению.
 ```
   # Выход функции со статусом по умолчанию 'EXECUTED'
[{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]

   # Выход функции, если вторым аргументов передано 'CANCELED'
[{'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]
 ```
6. Функция `sort_by_date` принимает список словарей и необязательный параметр, задающий порядок сортировки (по умолчанию — убывание),
   и возвращает новый список, отсортированный по дате (date).
```
   # Выход функции (сортировка по убыванию, т. е. сначала самые последние операции)
[{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
{'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}, 
{'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, 
{'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]
```
## Тестирование:

Проект покрыт юнит-тестами Pytest. Для их запуска выполните команду:
```
pytest tests
```
Информацию о покрытии кода тестами можно найти в файле [HTML](./htmlcov/index.html)

Процент покрытия на данный момент составляет 98%.

## Документация:

Для получения дополнительной информации обратитесь к [документации](PythonProject2/README.md)

## Лицензия:

Этот проект лицензирован по [лицензии MIT](LICENSE).

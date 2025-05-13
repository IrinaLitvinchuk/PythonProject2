from functools import wraps
from time import time


def log(filename=None):
    """Декоратор, который логирует работу функции и ее результат в файл (если указан) или выводит в консоль"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time()
            try:
                result = func(*args, **kwargs)
                finish_time = time()
                message = (f"{func.__name__} ok \n"
                           f"result = {result} \n"
                           f"Start: {start_time} \n"
                           f"Finish: {finish_time} \n")
            except Exception as e:
                finish_time = time()
                message = (f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs} \n"
                           f"Start: {start_time} \n"
                           f"Finish: {finish_time} \n")

                # Выводим сообщение в файл или в консоль
            if filename is not None:
                with open(filename, mode="a", encoding="utf-8") as file:
                    file.write(message)
            else:
                print(message)
            return func(*args, **kwargs)

        return wrapper

    return decorator


# Пример использования декоратора
# @log(filename=None)
# def my_function(x, y):
#     return x + y
#
#
# my_function(1, 2)
# Ожидаемый вывод в лог-файл mylog.txt при успешном выполнении:>>>my_function ok
# Ожидаемый вывод при ошибке:
#>>> my_function error: тип ошибки. Inputs: (1, 2), {}
# Где тип ошибки заменяется на текст ошибки.

# @log(filename="mylog.txt")
# def my_function(x, y):
#     return x / y
#
# my_function(1, 0)
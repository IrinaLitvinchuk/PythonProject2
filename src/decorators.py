from functools import wraps
from time import time
from typing import Any, Callable


def log(filename: Any = None) -> None:
    """Декоратор, который логирует работу функции и ее результат в файл (если указан) или выводит в консоль"""

    def decorator(func: Callable) -> Any:
        @wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> Any:
            start_time = time()
            try:
                result = func(*args, **kwargs)
                finish_time = time()
                message = (
                    f"{func.__name__} ok \n"
                    f"result = {result} \n"
                    f"Start: {start_time} \n"
                    f"Finish: {finish_time} \n"
                )
            except Exception as e:
                finish_time = time()
                message = (
                    f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs} \n"
                    f"Start: {start_time} \n"
                    f"Finish: {finish_time} \n"
                )

                # Выводим сообщение в файл или в консоль
            if filename is not None:
                with open(filename, mode="a", encoding="utf-8") as file:
                    file.write(message)
            else:
                print(message)
            return func(*args, **kwargs)

        return wrapper

    return

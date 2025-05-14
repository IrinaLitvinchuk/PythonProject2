from functools import wraps
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable[[Callable], Callable]:
    """Декоратор, который логирует работу функции и ее результат в файл (если указан) или выводит в консоль."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> Any:
            try:
                result = func(*args, **kwargs)
                message = f"{func.__name__} ok \n"
                if filename is not None:
                    with open(filename, mode="a", encoding="utf-8") as file:
                        file.write(message)
                else:
                    print(message)
                return result

            except Exception as e:
                message = f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs} \n"
                if filename is not None:
                    with open(filename, mode="a", encoding="utf-8") as file:
                        file.write(message)
                else:
                    print(message)
                raise

        return wrapper

    return decorator


# @log()
# def my_function(x, y):
#     return x / y
#
# my_function(1, 0)
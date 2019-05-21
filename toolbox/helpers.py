from collections import Callable
from functools import singledispatch, update_wrapper


class Equation:
    def __init__(self, key: str, value: Callable):
        self.key = key
        self.__value = value

    def __call__(self, *args, **kwargs):
        return self.__value(*args, **kwargs)

    def __str__(self):
        return self.key

    def __repr__(self):
        return f"Equation({self.key})"


def method_dispatch(func):
    dispatcher = singledispatch(func)

    def wrapper(*args, **kw):
        return dispatcher.dispatch(args[1].__class__)(*args, **kw)

    wrapper.register = dispatcher.register
    update_wrapper(wrapper, func)
    return wrapper

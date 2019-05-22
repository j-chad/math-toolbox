from collections import Callable
from functools import singledispatch, update_wrapper

__all__ = ["Equation"]


class Equation:
    """Represents an equation. Calling it with the values will return the value"""
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
    """A modification to the functools.singledispatch decorator that instead takes the 2nd argument.

    Intended for use in an instance method where the first argument will always be self.
    """
    dispatcher = singledispatch(func)

    def wrapper(*args, **kw):
        return dispatcher.dispatch(args[1].__class__)(*args, **kw)

    wrapper.register = dispatcher.register
    update_wrapper(wrapper, func)
    return wrapper

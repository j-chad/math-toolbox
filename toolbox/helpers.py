from collections import Callable


class Equation:
    def __init__(self, key: str, value: Callable):
        self.key = key
        self.__value = value

        self.__update_wrapper()

    def __call__(self, *args, **kwargs):
        return self.__value(*args, **kwargs)

    def __str__(self):
        return self.key

    def __repr__(self):
        return f"Equation({self.key})"

    # noinspection PyUnresolvedReferences
    def __update_wrapper(self):
        self.__call__.__annotations__ = self.__value.__annotations__
        self.__call__.__doc__ = self.__value.__doc__

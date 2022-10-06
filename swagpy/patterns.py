from .typing import Self


class Error(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(self.__doc__, *args)


class SingletonError(Error):
    """singleton type should not be instantiated"""


class Singleton:
    _instance = None

    def __init__(self) -> None:
        raise SingletonError

    def __new__(cls: type[Self]) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

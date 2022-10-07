from collections import namedtuple
from typing import Callable

from .typing import Self
from .exceptions import SingletonError


def _get_members(cls: type):
    def callback(func: Callable):
        return lambda *args, **kwargs: func(cls, *args, **kwargs)

    for key, value in vars(cls).items():
        if key.startswith("__"):
            continue
        if isinstance(value, Callable):
            value = callback(value)
        yield key, value


def frozen_singleton(cls: type[Self]) -> Self:
    members = dict(_get_members(cls))
    return namedtuple(cls.__name__, members.keys())(**members)


class Singleton:
    _instance = None

    def __init__(self) -> None:
        raise SingletonError

    def __new__(cls: type[Self]) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

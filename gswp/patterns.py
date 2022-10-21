__all__ = ["Singleton", "frozen_singleton"]
from collections import namedtuple
from typing import Callable, Iterable, get_type_hints

from .typing import Self
from .exceptions import SingletonError


def _get_members(cls: type):
    def callback(func: Callable):
        return lambda *args, **kwargs: func(cls, *args, **kwargs)

    for key, value in vars(cls).items():
        if key.startswith("_"):
            continue
        if isinstance(value, Callable):
            value = callback(value)
        yield key, value


def _repr_members(cls: type) -> Iterable:
    for key, value in vars(cls).items():
        if key.startswith("_"):
            continue
        if isinstance(value, Callable):
            hints = get_type_hints(value)

            return_value = hints.pop("return", None)
            args = ", ".join(f"{k}:{v.__name__}" for k, v in hints.items())
            yield f'{key}({args}) -> {return_value.__name__ if return_value else "Any"}'

        else:
            yield f"{key}:{type(value).__name__} = {value}"


def frozen_singleton(cls: type[Self]) -> Self:
    members = dict(_get_members(cls))

    class _SINGLETON(namedtuple(cls.__name__, members.keys())):
        __name__ = cls.__name__

        def __repr__(self) -> str:
            props = "\n  ".join(_repr_members(cls))
            return f"FROZEN[{cls.__name__}]:\n  {props}"

    return _SINGLETON(**members)

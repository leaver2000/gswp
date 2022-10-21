#
from enum import Enum, EnumMeta
from typing import (
    Callable,
    Generic,
    NewType,
    TypeVar,
    ParamSpec,
    Union,
    _GenericAlias,
    _type_repr,
)
import types
import functools


class StrEnum(str, Enum):
    ...


class _UnionGenericAlias(_GenericAlias, _root=True):
    # def copy_with(self, params):
    #     return Union[params]

    def __eq__(self, other):
        if not isinstance(other, (_UnionGenericAlias, types.UnionType)):
            return NotImplemented
        return set(self.__args__) == set(other.__args__)

    def __hash__(self):
        return hash(frozenset(self.__args__))

    def __repr__(self):
        args = self.__args__
        if len(args) == 2:
            if args[0] is type(None):
                return f"typing.Optional[{_type_repr(args[1])}]"
            elif args[1] is type(None):
                return f"typing.Optional[{_type_repr(args[0])}]"
        return super().__repr__()

    def __instancecheck__(self, obj):
        return self.__subclasscheck__(type(obj))

    def __subclasscheck__(self, cls):
        for arg in self.__args__:
            if issubclass(cls, arg):
                return True

    def __reduce__(self):
        func, (origin, args) = super().__reduce__()
        return func, (Union, args)


T1 = TypeVar("T1", bound=StrEnum)
T2 = TypeVar("T2", bound=StrEnum)
P = ParamSpec("P")
R = TypeVar("R")

_cleanups = []


def _typecache(func: Callable[P, R]) -> Callable[P, R]:
    """
    Internal wrapper caching __getitem__ of generic types with a fallback to
    original function for non-hashable arguments.
    """

    cached = functools.lru_cache(typed=True)(func)
    _cleanups.append(cached.cache_clear)

    @functools.wraps(func)
    def inner(*args: P.args, **kwds: P.kwargs):
        try:
            return cached(*args, **kwds)
        except TypeError:
            pass  # All real errors (not unhashable args) are raised below.
        return func(*args, **kwds)

    return inner


class _SpecialForm:
    __slots__ = ("_name", "__doc__", "_getitem")

    def __init__(self, getitem: type):
        self._getitem = getitem
        self._name = getitem.__name__
        self.__doc__ = getitem.__doc__

    def __getattr__(self, item):
        if item in {"__name__", "__qualname__"}:
            return self._name

        raise AttributeError(item)

    def __repr__(self):
        return self._name

    @_typecache
    def __getitem__(self, parameters: tuple[TypeVar, ...]):
        print(self, parameters)
        return self._getitem(self, parameters)


@_SpecialForm
class Inherited:
    def __new__(cls, form: type[_SpecialForm], parameters: tuple[TypeVar, ...]):
        return _UnionGenericAlias(form, parameters)


def extend(base: type[T1]):
    base_mapping = {member.name: member.value for member in base}

    def inner(cls: type[T2]) -> Inherited[T1, T2]:
        class_mapping = {member.name: member.value for member in cls}
        return StrEnum(cls.__name__, base_mapping | class_mapping)

    return inner


class GeosMeta(EnumMeta):
    def __instancecheck__(cls: "GeosType", instance: "GeosType") -> bool:

        return (
            super().__instancecheck__(instance)
            or isinstance(instance, GEOS.EAST)
            or isinstance(instance, GEOS.WEST)
        )


class GeosType(StrEnum, metaclass=GeosMeta):
    ABI_L1B_RADC = "ABI-L1b-RadC"
    ABI_L1B_RADF = "ABI-L1b-RadF"


class GEOS:
    @extend(GeosType)
    class WEST(StrEnum):
        ABI_L2_ACHAC = "ABI-L2-ACHAC"

    @extend(GeosType)
    class EAST(StrEnum):
        ABI_L2_AODC = "ABI-L2-AODC"


def main():

    assert isinstance(GEOS.EAST.ABI_L1B_RADC, GeosType)
    assert isinstance(GEOS.EAST.ABI_L1B_RADC, GEOS.EAST)

    assert isinstance(GEOS.WEST.ABI_L1B_RADC, GeosType)

    assert isinstance(GEOS.WEST.ABI_L1B_RADC, GEOS.WEST)

    assert not isinstance(GEOS.WEST, GEOS.EAST)

    assert (
        GEOS.WEST.ABI_L2_ACHAC not in GEOS.EAST and GEOS.WEST.ABI_L2_ACHAC in GEOS.WEST
    )


GEOS.EAST.ABI_L1B_RADC

GEOS.WEST.ABI_L1B_RADC
GEOS.WEST.ABI_L2_ACHAC

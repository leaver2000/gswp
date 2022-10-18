__all__ = [
    "Self",
    "floating1DArray",
    "unsignedinteger1DArray",
    "Properties",
    "Geometry",
    "Feature",
    "FeatureCollection",
    "TimeLike",
    "Array",
    "ndim",
    "dim",
]
from datetime import datetime
from typing import TypeVar, TypedDict, Literal, Generic
import pandas as pd
import numpy as np
from ..typing import dim as dim


Self = TypeVar("Self")
_DIM = TypeVar("_DIM", dim.one, dim.two, dim.three, dim.four, dim.five, dim.six, dim.N)
_DType = TypeVar("_DType")


class ndim(Generic[_DIM]):
    ...


_DimType = TypeVar("_DimType", bound=ndim)


class Array(Generic[_DType, _DimType]):
    ...


TimeLike = datetime | str | pd.Timestamp

GMGSIProducts = Literal["GMGSI_LW", "GMGSI_SSR", "GMGSI_SW", "GMGSI_VIS", "GMGSI_WV"]


class Properties(TypedDict):
    MUCAPE: int
    MLCAPE: int
    MLCIN: int
    EBSHEAR: float
    SRH01KM: int
    MESH: float
    VIL_DENSITY: float
    FLASH_RATE: int
    FLASH_DENSITY: float
    MAXLLAZ: float
    P98LLAZ: float
    P98MLAZ: float
    MAXRC_EMISS: str
    MAXRC_ICECF: str
    WETBULB_0C_HGT: float
    PWAT: float
    CAPE_M10M30: int
    LJA: float
    SIZE: int
    AVG_BEAM_HGT: str
    MOTION_EAST: float
    MOTION_SOUTH: float
    PS: int
    ID: int


class Geometry(TypedDict):
    type: Literal["Polygon"]
    coordinates: list[list[tuple[float, float]]]


class Feature(TypedDict):
    type: Literal["Feature"]
    geometry: Geometry
    models: dict[str, dict[str, str]]
    properties: Properties


class FeatureCollection(TypedDict):
    source: Literal["NOAA/NCEP Central Operations"]
    product: Literal["ProbSevere"]
    type: Literal["FeatureCollection"]
    validTime: str
    productionTime: str
    machine: str
    features: list[Feature]

__all__ = ["Store"]
from datetime import datetime
from pathlib import Path
from typing import Literal
import xarray as xr

from .patterns import frozen_singleton
from .typing import GMGSIProducts
MRMS_BOUNDS = (-130, -60, 20, 55)
"""CONUS MRMS BOUNDS (W, E, S, N) """


@frozen_singleton
class STORE:
    """store for various directories"""

    DATA = Path.cwd().parent / "data"
    GMGSI = DATA / "GMGSI"
    """Global Mosaic of Geostationary Satellite Imagery (GMGSI) Product"""
    GMGSI_LW = GMGSI / "LONGWAVE"
    GMGSI_SW = GMGSI /"SHORTWAVE"
    GMGSI_WV =  GMGSI /"WATERVAPOR"
    GMGSI_VIS =  GMGSI /"VISIBLE"

    PROBSEVERE = DATA / "PROBSEVERE"
    """NOAA/CIMMS ProbSevere"""
    GSWR = DATA / "GSWR"


@frozen_singleton
class PROBSEVERE:
    """NOAA/CIMMS ProbSevere"""

    STORE = STORE.PROBSEVERE
    #
    VALIDTIME_TEMPLATE = "%Y%m%d_%H%M%S %Z"
    #
    EBSHEAR = "EBSHEAR"
    MEANWIND = "MEANWIND_1-3kmAGL"
    MESH = "MESH"
    VIL_DENSITY = "VIL_DENSITY"
    FLASH_DENSITY = "FLASH_DENSITY"
    MOTION_EAST = "MOTION_EAST"
    MOTION_SOUTH = "MOTION_SOUTH"
    MAXLLAZ = "MAXLLAZ"
    P98LLAZ = "P98LLAZ"
    P98MLAZ = "P98MLAZ"
    WETBULB_0C_HGT = "WETBULB_0C_HGT"
    PWAT = "PWAT"
    LJA = "LJA"
    FLOAT32 = frozenset(
        (
            EBSHEAR,
            MEANWIND,
            MESH,
            VIL_DENSITY,
            FLASH_DENSITY,
            MOTION_EAST,
            MOTION_SOUTH,
            MAXLLAZ,
            P98LLAZ,
            P98MLAZ,
            WETBULB_0C_HGT,
            PWAT,
            LJA,
        )
    )
    #
    MLCIN = "MLCIN"
    INT32 = frozenset((MLCIN,))
    #
    MUCAPE = "MUCAPE"
    MLCAPE = "MLCAPE"
    SRH01KM = "SRH01KM"
    FLASH_RATE = "FLASH_RATE"
    CAPE_M10M30 = "CAPE_M10M30"
    SIZE = "SIZE"
    ID = "ID"
    UINT32 = frozenset(
        (
            MUCAPE,
            MLCAPE,
            SRH01KM,
            FLASH_RATE,
            CAPE_M10M30,
            SIZE,
            ID,
        )
    )
    #
    PS = "PS"
    UINT8 = frozenset((PS,))
    #
    PARAMETERS = UINT8.union(UINT32).union(INT32).union(FLOAT32)
    MINX = "minx"
    MINY = "miny"
    MAXX = "maxx"
    MAXY = "maxy"
    X = "x"
    Y = "y"
    GEOMETRY = frozenset((MINX, MINY, MAXX, MAXY, X, Y))
    def column_dtypes(self):
        return (
            list(self.FLOAT32.union(self.GEOMETRY)),
            list(self.INT32),
            list(self.UINT32),
            list(self.UINT8),
        )
    def load(self) -> xr.Dataset:
        return xr.open_zarr(self.STORE)


@frozen_singleton
class GMGSI:
    LONG_WAVE = "GMGSI_LW"
    SHORT_WAVE = "GMGSI_SW"
    WATER_VAPOR = "GMGSI_WV"
    VISIBLE = "GMGSI_VIS"
    STORE = STORE.GMGSI
    PARAMETERS = frozenset((LONG_WAVE, SHORT_WAVE, WATER_VAPOR, VISIBLE))
    DIRECTORY = dict(zip(PARAMETERS,("LONGWAVE","SHORTWAVE","WATERVAPOR","VISIBLE")))

    def load(self) -> xr.Dataset:
        import dask
        def generate():
            for path in self.DIRECTORY.values():
                store = self.STORE / path
                if not store.exists():
                    continue
                yield xr.open_zarr(store)
        with dask.config.set(**{"array.slicing.split_large_chunks": True}):
            return xr.merge(generate())
        # return xr.merge([xr.open_zarr(self.STORE / path) for path in self.DIRECTORY.values()])

    def url(self, product:GMGSIProducts, date:datetime) -> str:
        return f"s3://noaa-gmgsi-pds/{product}/{date:%Y}/{date:%m}/{date:%d}"



@frozen_singleton
class ATMOSPHERE:
    ABSOLUTE_ZERO = -273.15

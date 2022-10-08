__all__ = ["Store"]
from pathlib import Path
import xarray as xr

from .patterns import frozen_singleton

MRMS_BOUNDS = (-130, -60, 20, 55)
"""CONUS MRMS BOUNDS (W, E, S, N) """


@frozen_singleton
class STORE:
    """store for various directories"""

    DATA = Path.cwd().parent / "data"
    GMGSI = DATA / "GMGSI"
    """Global Mosaic of Geostationary Satellite Imagery (GMGSI) Product"""
    PROBSEVERE = DATA / "PROBSEVERE"
    """NOAA/CIMMS ProbSevere"""
    GSWR = DATA / "GSWR"


@frozen_singleton
class PROBSEVERE:
    """NOAA/CIMMS ProbSevere"""

    STORE = STORE.PROBSEVERE

    VALIDTIME_TEMPLATE = "%Y%m%d_%H%M%S %Z"

    FLOAT32 = (
        "EBSHEAR",
        "MEANWIND_1-3kmAGL",
        "MESH",
        "VIL_DENSITY",
        "FLASH_DENSITY",
        "MOTION_EAST",
        "MOTION_SOUTH",
        "MAXLLAZ",
        "P98LLAZ",
        "P98MLAZ",
        "WETBULB_0C_HGT",
        "PWAT",
        "LJA",
    )

    INT32 = ("MLCIN",)

    UINT32 = (
        "MUCAPE",
        "MLCAPE",
        "SRH01KM",
        "FLASH_RATE",
        "CAPE_M10M30",
        "SIZE",
        "ID",
    )

    UINT8 = ("PS",)

    PARAMETERS = UINT8 + UINT32 + INT32 + FLOAT32
    GEOMETRY = ("minx", "miny", "maxx", "maxy", "x", "y")

    def load(self) -> xr.Dataset:
        return xr.open_zarr(self.STORE)


@frozen_singleton
class GMGSI:
    STORE = STORE.GMGSI

    def load(self):
        return xr.open_zarr(self.STORE)

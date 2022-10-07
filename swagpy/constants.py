__all__ = ["Store"]
from pathlib import Path
from .patterns import frozen_singleton

MRMS_BOUNDS = (-130, -60, 20, 55)
"""CONUS MRMS BOUNDS (W, E, S, N) """


@frozen_singleton
class Store:
    """store for various directories"""

    data = Path.cwd().parent / "data"
    gmgsi = data / "GMGSI"
    """Global Mosaic of Geostationary Satellite Imagery (GMGSI) Product"""
    probsevere = data / "PROBSEVERE"
    gswr = data / "GSWR"


@frozen_singleton
class PROBSEVERE:
    """probsevere dataset constants"""

    store = Store.probsevere
    validtime_template = "%Y%m%d_%H%M%S %Z"

    float32 = (
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

    int32 = ("MLCIN",)

    uint32 = (
        "MUCAPE",
        "MLCAPE",
        "SRH01KM",
        "FLASH_RATE",
        "CAPE_M10M30",
        "SIZE",
        "ID",
    )

    uint8 = ("PS",)

    all_columns = uint8 + uint32 + int32 + float32
    geometry = ("MINX", "MINY", "MAXX", "MAXY", "X", "Y")

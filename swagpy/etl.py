__all__ = ["probsevere", "gmgsi"]
from datetime import datetime
from pathlib import Path
from typing import Iterable, Literal
import io
import warnings

import s3fs
import requests
from requests import Session, HTTPError

import xarray as xr
import pandas as pd
import numpy as np
from geopandas import GeoDataFrame

from .typing import FeatureCollection, TimeLike
from .patterns import Singleton

GMGSIProducts = Literal["GMGSI_LW", "GMGSI_SSR", "GMGSI_SW", "GMGSI_VIS", "GMGSI_WV"]

FLOAT32_COLS = [
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
]

INT32_COLS = ["MLCIN"]

UINT32_COLS = [
    "MUCAPE",
    "MLCAPE",
    "SRH01KM",
    "FLASH_RATE",
    "CAPE_M10M30",
    "SIZE",
    "ID",
]

UINT8_COLS = ["PS"]

ALL_COLUMNS = UINT8_COLS + UINT32_COLS + INT32_COLS + FLOAT32_COLS
VALIDTIME_TEMPLATE = "%Y%m%d_%H%M%S %Z"


class Extract(Singleton):
    @classmethod
    def probsevere(cls, date: TimeLike) -> Iterable[FeatureCollection]:
        base_url = "https://mtarchive.geol.iastate.edu"
        url = f"{base_url}/{date:%Y}/{date:%m}/{date:%d}/mrms/ncep/ProbSevere/"
        r = requests.get(url)
        if r.status_code == 200:
            (df,) = pd.read_html(r.text, skiprows=[1, 2], keep_default_na=False)

            with Session() as session:
                for file in tuple(url + df.loc[df["Name"] != "", "Name"]):
                    try:
                        # with our session make a get request, r is a response object
                        r = session.get(file, stream=True)
                        # in the event of a non 200 status code we'll raise a HTTPError and trigger the except block
                        r.raise_for_status()
                    # if there was an error downloading, continue
                    except (ConnectionError, HTTPError):
                        warnings.warn(f"error downloading {url}")
                        continue
                    yield r.json()

    @classmethod
    def gmgsi(
        cls,
        date: datetime,
        product: GMGSIProducts,
    ):
        fs = s3fs.S3FileSystem(anon=True)

        url_path = f"s3://noaa-gmgsi-pds/{product}/{date:%Y}/{date:%m}/{date:%d}"

        def open_dataset(file):
            with fs.open(file, "rb") as f:
                return xr.open_dataset(
                    io.BytesIO(f.read()), engine="h5netcdf", chunks={}
                )

        for path in fs.ls(url_path):
            for file in fs.ls(path):
                yield open_dataset(file)


class Transfer(Singleton):
    @classmethod
    def probsevere(cls, data: Iterable[FeatureCollection]) -> xr.Dataset:
        def geodataframes():
            for fc in data:
                df = GeoDataFrame.from_features(
                    fc["features"], columns=ALL_COLUMNS + ["geometry"]
                )
                df["time"] = datetime.strptime(fc["validTime"], VALIDTIME_TEMPLATE)
                yield df

        def wrangle_geometry(df: GeoDataFrame) -> pd.DataFrame:
            # to keep things consistent uppercase all of the bounds
            bounds = df.bounds
            df[bounds.columns.str.upper()] = bounds
            with warnings.catch_warnings():
                # /opt/conda/envs/rapids/lib/python3.9/site-packages/geopandas/array.py:524:
                # ShapelyDeprecationWarning: The array interface is deprecated and will no longer work in Shapely 2.0. Convert the '.coords' to a numpy array instead.
                #   return GeometryArray(vectorized.representative_point(self.data), crs=self.crs)
                warnings.simplefilter("ignore")
                points = df.representative_point()
            df["Y"] = points.x
            df["X"] = points.y
            return df.drop(columns="geometry")

        df = pd.concat(geodataframes()).set_index("time").pipe(wrangle_geometry)


        float32_cols = FLOAT32_COLS + ["MINX", "MINY", "MAXX", "MAXY", "X", "Y"]
        df[float32_cols] = df[float32_cols].astype(np.float32)
        # 32-bit-precision floating-point number type: sign bit, 8 bits exponent, 23 bits mantissa.
        df[INT32_COLS] = df[INT32_COLS].astype(np.int32)
        # 32-bit signed integer (``-2_147_483_648`` to ``2_147_483_647``)
        df[UINT32_COLS] = df[UINT32_COLS].astype(np.uint32)
        # 32-bit unsigned integer (``0`` to ``4_294_967_295``)
        df[UINT8_COLS] = df[UINT8_COLS].astype(np.uint8)
        # numpy.uint8`: 8-bit unsigned integer (``0`` to ``255``)
        return xr.Dataset.from_dataframe(df)

    @classmethod
    def gmgsi(
        cls,
        objs: Iterable[xr.Dataset],
        product: GMGSIProducts = "GMGSI_LW",
    ) -> xr.Dataset:
        ds = xr.concat(objs, dim="time")
        ds["yc"] = np.unique(ds.lat)
        ds["xc"] = np.unique(ds.lon)
        return ds.drop(["lat", "lon"]).rename(
            {"xc": "lon", "yc": "lat", "data": product}
        )


def load(ds: xr.Dataset, store: Path) -> None:
    zarr_kwargs = {}
    if store.exists():
        zarr_kwargs = {"mode": "a", "append_dim": "time"}
    ds.to_zarr(store, **zarr_kwargs)


def probsevere(
    start: datetime,
    end: datetime,
    /,
    store: Path = ...,
) -> None:
    if not isinstance(store, Path):
        raise Exception
    for date in pd.date_range(start, end, freq="D"):
        # extract
        collection = Extract.probsevere(date)
        # transfer
        ds = Transfer.probsevere(collection)
        # load
        load(ds, store)


def gmgsi(
    start: datetime,
    end: datetime,
    /,
    product: GMGSIProducts = "GMGSI_LW",
    store: Path = None,
) -> None:
    if not isinstance(store, Path):
        raise Exception
    for date in pd.date_range(start, end, freq="D"):
        # extract
        collection = Extract.gmgsi(date, product)
        # transfer
        ds = Transfer.gmgsi(collection, product)
        # load
        load(ds, store)

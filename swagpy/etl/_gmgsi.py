__all__ = ["extract", "transfer", "load", "main"]
from datetime import datetime
from pathlib import Path
from typing import Iterable
import io

import s3fs

import xarray as xr
import pandas as pd
import numpy as np

from ..typing import GMGSIProducts


def transfer(
    objs: Iterable[xr.Dataset],
    product: GMGSIProducts = "GMGSI_LW",
) -> xr.Dataset:
    ds = xr.concat(objs, dim="time")
    ds["yc"] = np.unique(ds.lat)
    ds["xc"] = np.unique(ds.lon)
    return ds.drop(["lat", "lon"]).rename({"xc": "lon", "yc": "lat", "data": product})


def extract(
    date: datetime,
    product: GMGSIProducts,
):
    fs = s3fs.S3FileSystem(anon=True)

    url_path = f"s3://noaa-gmgsi-pds/{product}/{date:%Y}/{date:%m}/{date:%d}"

    def open_dataset(file):
        with fs.open(file, "rb") as f:
            return xr.open_dataset(io.BytesIO(f.read()), engine="h5netcdf", chunks={})

    for path in fs.ls(url_path):
        for file in fs.ls(path):
            yield open_dataset(file)


def load(ds: xr.Dataset, store: Path) -> None:
    zarr_kwargs = {}
    if store.exists():
        zarr_kwargs = {"mode": "a", "append_dim": "time"}
    ds.to_zarr(store, **zarr_kwargs)


def main(
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
        collections = extract(date, product)
        # transfer
        ds = transfer(collections, product)
        # load
        load(ds, store)

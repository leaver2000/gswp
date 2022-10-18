__all__ = ["extract", "transfer", "main"]
from datetime import datetime
from pathlib import Path
from typing import Iterable
import io

import s3fs

import xarray as xr
import pandas as pd
import numpy as np
from ..constants import GMGSI
from ..typing import GMGSIProducts


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


def transfer(
    objs: Iterable[xr.Dataset],
    product: GMGSIProducts,
) -> xr.Dataset:
    ds = xr.concat(objs, dim="time")
    ds["yc"] = np.unique(ds.lat)
    ds["xc"] = np.unique(ds.lon)
    return ds.drop(["lat", "lon"]).rename({"xc": "lon", "yc": "lat", "data": product})


def main(
    start: datetime,
    end: datetime,
    /,
    product: GMGSIProducts = GMGSI.LONG_WAVE,
    store: Path = GMGSI.STORE,
) -> None:
    if product not in GMGSI.PARAMETERS:
        raise Exception

    if not GMGSI.STORE.exists():
        GMGSI.STORE.mkdir()
    # products are nested in the store due to conflicts with times
    store = store / GMGSI.DIRECTORY[product]
    append_dim = None
    for date in pd.date_range(start, end, freq="D"):
        # extract - one full days worth of data for a single gmgsi product
        collections = extract(date, product)
        # transfer - concat the data into a single dataset
        ds = transfer(collections, product)
        # load - the dataset to the product store
        try:
            ds.to_zarr(store, mode="a", append_dim=append_dim)
        except ValueError:
            append_dim = "time"
            ds.to_zarr(store, mode="a", append_dim=append_dim)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--start")
    parser.add_argument("--end")
    parser.add_argument("--product")
    parser.add_argument("--store")
    args = parser.parse_args()
    main(args.start, args.end, args.product, args.store)

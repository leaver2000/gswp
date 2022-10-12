__all__ = ["extract", "transfer", "load", "main"]
from datetime import datetime
from pathlib import Path
from typing import Iterable
import warnings

import requests
from requests import Session, HTTPError

import xarray as xr
import pandas as pd
import numpy as np
from geopandas import GeoDataFrame

from ..typing import FeatureCollection, TimeLike
from ..constants import PROBSEVERE


def extract(date: TimeLike) -> Iterable[FeatureCollection]:
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


def transfer(data: Iterable[FeatureCollection]) -> xr.Dataset:
    def geodataframes():
        for fc in data:
            df = GeoDataFrame.from_features(
                fc["features"], columns=list(PROBSEVERE.PARAMETERS.union(("geometry",)))
            )
            df["time"] = datetime.strptime(
                fc["validTime"], PROBSEVERE.VALIDTIME_TEMPLATE
            )
            yield df

    def wrangle_geometry(df: GeoDataFrame) -> pd.DataFrame:
        # to keep things consistent uppercase all of the bounds
        df[df.bounds.columns] = df.bounds
        with warnings.catch_warnings():
            # /opt/conda/envs/rapids/lib/python3.9/site-packages/geopandas/array.py:524:
            # ShapelyDeprecationWarning: The array interface is deprecated and will no longer work in Shapely 2.0. Convert the '.coords' to a numpy array instead.
            #   return GeometryArray(vectorized.representative_point(self.data), crs=self.crs)
            warnings.simplefilter("ignore")
            points = df.representative_point()
        df["x"] = points.x
        df["y"] = points.y
        return df.drop(columns="geometry")

    df = pd.concat(geodataframes()).set_index("time").pipe(wrangle_geometry)

    float32, int32, uint32, uint8 = PROBSEVERE.column_dtypes()
    df[float32] = df[float32].astype(np.float32)
    # 32-bit-precision floating-point number type: sign bit, 8 bits exponent, 23 bits mantissa.
    df[int32] = df[int32].astype(np.int32)
    # 32-bit signed integer (``-2_147_483_648`` to ``2_147_483_647``)
    df[uint32] = df[uint32].astype(np.uint32)
    # 32-bit unsigned integer (``0`` to ``4_294_967_295``)
    df[uint8] = df[uint8].astype(np.uint8)
    # numpy.uint8`: 8-bit unsigned integer (``0`` to ``255``)
    return xr.Dataset.from_dataframe(df)


def load(ds: xr.Dataset, store: Path) -> None:
    append_dim = None
    if store.exists():
        append_dim = "time"
    ds.to_zarr(store, append_dim=append_dim)


def main(
    start: datetime,
    end: datetime,
    /,
    store: Path = PROBSEVERE.STORE,
) -> None:
    if not isinstance(store, Path):
        raise Exception

    for date in pd.date_range(start, end, freq="D"):
        # extract
        collection = extract(date)
        # transfer
        ds = transfer(collection)
        # load
        load(ds, store)

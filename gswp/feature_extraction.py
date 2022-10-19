# FITTING TIME
from typing import Iterable

import numpy as np
import pandas as pd
import xarray as xr
import dask


INTERVAL = 60
TIME_RANGE = 1
TIME="time"

def constrain_bounds(
    ds: xr.Dataset, w: float, e: float, s: float, n: float
) -> xr.Dataset:
    with dask.config.set(**{"array.slicing.split_large_chunks": True}):
        lat, lon = ds.lat, ds.lon
        indexers = {
            "lat": lat[(lat > s) & (lat < n)],
            "lon": lon[(lon > w) & (lon < e)],
        }
        return ds.sel(indexers)


def unpack_datetimeindex(*args: np.ndarray) ->Iterable[pd.DatetimeIndex]:
    for da in args:
        yield pd.to_datetime(da)


def fit_times(
    ps: xr.Dataset, gmgsi: xr.Dataset, interval=INTERVAL, time_range=TIME_RANGE
) -> tuple[xr.Dataset, ...]:
    # normalize the time dtypes by shaving off seconds
    ps[TIME] = ps[TIME].astype("datetime64[m]")
    gmgsi[TIME] = gmgsi[TIME].astype("datetime64[m]")

    with dask.config.set(**{"array.slicing.split_large_chunks": True}):
        # slice an interval of the probsevere data
        ps.sel(
            time=(pd.to_datetime(ps[TIME].to_numpy()).minute % interval) < time_range
        )
        gmgsi_time, ps_time = unpack_datetimeindex(
            gmgsi[TIME].to_numpy(), ps[TIME].to_numpy()
        )

        return (
            ps.sel(time=ps_time.isin(gmgsi_time)),
            gmgsi.sel(time=gmgsi_time.isin(ps_time)),
        )

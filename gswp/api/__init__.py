__all__ = ["extract_features", "minimum_diffrence"]
# cythonize -i swagpy/api/_api.pyx
from typing import NewType
import numpy as np
import dask.array as da

from ..api._api import extract_features

_1D = NewType("1d", tuple)
_2D = NewType("2d", tuple)


def minimum_diffrence(
    target: np.ndarray[_1D, np.floating],
    values: np.ndarray[_1D, np.floating],
    engine="dask",
) -> da.Array | np.ndarray:
    target = target[:, np.newaxis]
    if engine == "dask":
        diff = abs(da.array(target) - da.array(values))
        return da.argmin(diff, axis=0)
    else:
        diff = abs(target - values)
        return np.argmin(diff, axis=0)

__all__ = ["extract_features"]
from typing import NewType
import numpy as np

D2 = NewType("D2", tuple[int, int])
D1 = NewType("D1", tuple[int])

def extract_features(
    arr: np.ndarray[D2, np.floating],
    min_lat: np.ndarray[D2, np.unsignedinteger],
    max_lat: np.ndarray[D2, np.unsignedinteger],
    min_lon: np.ndarray[D2, np.unsignedinteger],
    max_lon: np.ndarray[D2, np.unsignedinteger],
) -> list[np.ndarray[D2, np.floating]]: ...

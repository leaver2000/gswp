import numpy as np
cimport numpy as np

def extract_features(
    np.ndarray[np.float32_t, ndim=2] arr,
    np.ndarray[np.long_t, ndim=1] min_lon,
    np.ndarray[np.long_t, ndim=1] max_lon,
    np.ndarray[np.long_t, ndim=1] min_lat,
    np.ndarray[np.long_t, ndim=1] max_lat
):
    result = [
        arr[x1:x2, y1:y2]
        for x1, x2, y1, y2 in np.c_[min_lat, max_lat, min_lon, max_lon]
    ]
    
    return result
    
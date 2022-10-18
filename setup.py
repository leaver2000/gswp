from setuptools import setup, Extension

from pathlib import Path

import numpy as np

GWSP = Path.cwd() / "gwsp"
API = GWSP / "api"

a = np.array([], dtype=float)


ext_modules = [
    Extension(
        "gswp.api._api",
        sources=[str(file) for file in API.glob("*.pyx")],
        include_dirs=[np.get_include()],
        )
]


setup(
    ext_modules=ext_modules,
)

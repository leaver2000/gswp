from setuptools import setup, Extension
from pathlib import Path
import numpy as np
SWAG = Path.cwd() / "swagpy"
API = SWAG / "api"


ext_modules = [
        Extension(
            "swagpy.api._api",
            sources=[str(file) for file in API.glob("*.pyx")],
            include_dirs=[np.get_include()],
        )
    ]
setup(
    ext_modules=ext_modules,
)

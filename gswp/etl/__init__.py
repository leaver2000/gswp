__all__ = ["gmgsi", "probsevere"]
from pathlib import Path
from datetime import datetime
from .typing import GMGSIProducts
from ..etl import _gmgsi, _probsevere


def gmgsi(
    start: datetime, end: datetime, product: GMGSIProducts, store: Path = None
) -> None:
    """download and extract gmgsi data"""
    _gmgsi.main(start, end, product, store=None)


def probsevere(start: datetime, end: datetime, store: Path = None) -> None:
    """download and extract probsevere data"""
    _probsevere.main(start, end, store)

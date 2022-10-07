__all__ = ["data", "gmgsi", "probsevere", "gswr"]
from pathlib import Path

data = Path(__file__).parents[1] / "data"


gmgsi = data / "GMGSI"
probsevere = data / "PROBSEVERE"
gswr = data / "GSWR"

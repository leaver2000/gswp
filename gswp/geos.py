__all__ = ["EAST", "WEST", "HIMAWARI"]

from enum import Enum, EnumMeta
from typing import NamedTuple, TypeVar


class StrEnum(str, Enum):
    ...


T = TypeVar("T", bound=StrEnum)


class GeosMeta(EnumMeta):
    def __instancecheck__(cls: "GeosType", instance: "GeosType") -> bool:

        return (
            super().__instancecheck__(GeosType)
            or isinstance(instance, GEOS.EAST)
            or isinstance(instance, GEOS.WEST)
        )


class GeosType(StrEnum, metaclass=GeosMeta):
    ABI_L1B_RADC = "ABI-L1b-RadC"
    ABI_L1B_RADF = "ABI-L1b-RadF"
    ABI_L1B_RADM = "ABI-L1b-RadM"
    ABI_L2_ACHAC = "ABI-L2-ACHAC"
    ABI_L2_ACHAF = "ABI-L2-ACHAF"
    ABI_L2_ACHAM = "ABI-L2-ACHAM"
    ABI_L2_ACHTF = "ABI-L2-ACHTF"
    ABI_L2_ACHTM = "ABI-L2-ACHTM"
    ABI_L2_ACMC = "ABI-L2-ACMC"
    ABI_L2_ACMF = "ABI-L2-ACMF"
    ABI_L2_ACMM = "ABI-L2-ACMM"
    ABI_L2_ACTPC = "ABI-L2-ACTPC"
    ABI_L2_ACTPF = "ABI-L2-ACTPF"
    ABI_L2_ACTPM = "ABI-L2-ACTPM"
    ABI_L2_ADPC = "ABI-L2-ADPC"
    ABI_L2_ADPF = "ABI-L2-ADPF"
    ABI_L2_ADPM = "ABI-L2-ADPM"
    ABI_L2_AICEF = "ABI-L2-AICEF"
    ABI_L2_AITAF = "ABI-L2-AITAF"
    ABI_L2_AODC = "ABI-L2-AODC"
    ABI_L2_AODF = "ABI-L2-AODF"
    ABI_L2_BRFC = "ABI-L2-BRFC"
    ABI_L2_BRFF = "ABI-L2-BRFF"
    ABI_L2_BRFM = "ABI-L2-BRFM"
    ABI_L2_CMIPC = "ABI-L2-CMIPC"
    ABI_L2_CMIPF = "ABI-L2-CMIPF"
    ABI_L2_CMIPM = "ABI-L2-CMIPM"
    ABI_L2_CODC = "ABI-L2-CODC"
    ABI_L2_CODF = "ABI-L2-CODF"
    ABI_L2_CPSC = "ABI-L2-CPSC"
    ABI_L2_CPSF = "ABI-L2-CPSF"
    ABI_L2_CPSM = "ABI-L2-CPSM"
    ABI_L2_CTPC = "ABI-L2-CTPC"
    ABI_L2_CTPF = "ABI-L2-CTPF"
    ABI_L2_DMWC = "ABI-L2-DMWC"
    ABI_L2_DMWF = "ABI-L2-DMWF"
    ABI_L2_DMWM = "ABI-L2-DMWM"
    ABI_L2_DMWVC = "ABI-L2-DMWVC"
    ABI_L2_DMWVF = "ABI-L2-DMWVF"
    ABI_L2_DMWVM = "ABI-L2-DMWVM"
    ABI_L2_DSIC = "ABI-L2-DSIC"
    ABI_L2_DSIF = "ABI-L2-DSIF"
    ABI_L2_DSIM = "ABI-L2-DSIM"
    ABI_L2_DSRC = "ABI-L2-DSRC"
    ABI_L2_DSRF = "ABI-L2-DSRF"
    ABI_L2_DSRM = "ABI-L2-DSRM"
    ABI_L2_FDCC = "ABI-L2-FDCC"
    ABI_L2_FDCF = "ABI-L2-FDCF"
    ABI_L2_FDCM = "ABI-L2-FDCM"
    ABI_L2_LSAC = "ABI-L2-LSAC"
    ABI_L2_LSAF = "ABI-L2-LSAF"
    ABI_L2_LSAM = "ABI-L2-LSAM"
    ABI_L2_LST2KMF = "ABI-L2-LST2KMF"
    ABI_L2_LSTC = "ABI-L2-LSTC"
    ABI_L2_LSTF = "ABI-L2-LSTF"
    ABI_L2_LSTM = "ABI-L2-LSTM"
    ABI_L2_LVMPC = "ABI-L2-LVMPC"
    ABI_L2_LVMPF = "ABI-L2-LVMPF"
    ABI_L2_LVMPM = "ABI-L2-LVMPM"
    ABI_L2_LVTPC = "ABI-L2-LVTPC"
    ABI_L2_LVTPF = "ABI-L2-LVTPF"
    ABI_L2_LVTPM = "ABI-L2-LVTPM"
    ABI_L2_MCMIPC = "ABI-L2-MCMIPC"
    ABI_L2_MCMIPF = "ABI-L2-MCMIPF"
    ABI_L2_MCMIPM = "ABI-L2-MCMIPM"
    ABI_L2_RRQPEF = "ABI-L2-RRQPEF"
    ABI_L2_RSRC = "ABI-L2-RSRC"
    ABI_L2_RSRF = "ABI-L2-RSRF"
    ABI_L2_SSTF = "ABI-L2-SSTF"
    ABI_L2_TPWC = "ABI-L2-TPWC"
    ABI_L2_TPWF = "ABI-L2-TPWF"
    ABI_L2_TPWM = "ABI-L2-TPWM"
    ABI_L2_VAAF = "ABI-L2-VAAF"
    EXIS_L1B_SFEU = "EXIS-L1b-SFEU"
    EXIS_L1B_SFXR = "EXIS-L1b-SFXR"
    GLM_L2_LCFA = "GLM-L2-LCFA"
    MAG_L1B_GEOF = "MAG-L1b-GEOF"
    SEIS_L1B_EHIS = "SEIS-L1b-EHIS"
    SEIS_L1B_MPSH = "SEIS-L1b-MPSH"
    SEIS_L1B_MPSL = "SEIS-L1b-MPSL"
    SEIS_L1B_SGPS = "SEIS-L1b-SGPS"
    SUVI_L1B_FE093 = "SUVI-L1b-Fe093"
    SUVI_L1B_FE131 = "SUVI-L1b-Fe131"
    SUVI_L1B_FE171 = "SUVI-L1b-Fe171"
    SUVI_L1B_FE195 = "SUVI-L1b-Fe195"
    SUVI_L1B_FE284 = "SUVI-L1b-Fe284"
    SUVI_L1B_HE303 = "SUVI-L1b-He303"


def strenum(name: str, tp: type[T], **kwargs: str) -> T:
    return StrEnum(name, {member.name: member.value for member in tp} | kwargs)


class GEOS(NamedTuple):
    WEST: GeosType
    EAST: GeosType


GEOS = GEOS(strenum("WEST", GeosType), strenum("EAST", GeosType))


class HIMAWARI(StrEnum):
    AHI_L1B_FLDK = "AHI-L1b-FLDK"
    AHI_L1B_JAPAN = "AHI-L1b-Japan"
    AHI_L1B_TARGET = "AHI-L1b-Target"
    AHI_L2_FLDK_CLOUDS = "AHI-L2-FLDK-Clouds"
    AHI_L2_FLDK_ISATSS = "AHI-L2-FLDK-ISatSS"
    AHI_L2_FLDK_RAINFALLRATE = "AHI-L2-FLDK-RainfallRate"
    AHI_L2_FLDK_SST = "AHI-L2-FLDK-SST"
    AHI_L2_FLDK_WINDS = "AHI-L2-FLDK-Winds"

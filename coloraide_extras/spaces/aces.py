"""
ACES colors.

https://www.oscars.org/science-technology/aces/aces-documentation
"""
import math
from coloraide.gamut.bounds import GamutBound
from coloraide.spaces.srgb import SRGB
from coloraide import algebra as alg
from coloraide.types import Vector
from typing import Tuple

AP0_TO_XYZ = [
    [0.9525523959381857, 0.0, 9.367863166046855e-05],
    [0.34396644976507507, 0.7281660966134857, -0.07213254637856079],
    [0.0, 0.0, 1.0088251843515859]
]

XYZ_TO_AP0 = [
    [1.0498110174979742, 0.0, -9.748454057925287e-05],
    [-0.49590302307731976, 1.3733130458157063, 0.09824003605730998],
    [0.0, 0.0, 0.991252018200499]
]

AP1_TO_XYZ = [
    [0.6624541811085053, 0.13400420645643313, 0.1561876870049078],
    [0.27222871678091454, 0.6740817658111484, 0.05368951740793705],
    [-0.005574649490394108, 0.004060733528982826, 1.0103391003129971]
]

XYZ_TO_AP1 = [
    [1.6410233796943257, -0.32480329418479, -0.23642469523761225],
    [-0.6636628587229829, 1.6153315916573379, 0.016756347685530137],
    [0.011721894328375376, -0.008284441996237409, 0.9883948585390215]
]

MIN = 0.0
MAX = 1.0
CG_MIN = 0.0
CG_MAX = 1.0
CC_MIN = -0.35828683
CC_MAX = (math.log2(65504) + 9.72) / 17.52
CCT_MIN = 0.0729055341958355
CCT_MAX = CC_MAX
CONST1 = 2 ** -16
CONST2 = 2 ** -15
CONST3 = (9.72 - 15) / 17.52


def aces_to_xyz(aces: Vector) -> Vector:
    """Convert ACEScc to XYZ."""

    return alg.dot(AP0_TO_XYZ, aces, dims=alg.D2_D1)


def xyz_to_aces(xyz: Vector) -> Vector:
    """Convert XYZ to ACEScc."""

    return alg.dot(XYZ_TO_AP0, xyz, dims=alg.D2_D1)


def acescg_to_xyz(acescg: Vector) -> Vector:
    """Convert ACEScc to XYZ."""

    return alg.dot(AP1_TO_XYZ, acescg, dims=alg.D2_D1)


def xyz_to_acescg(xyz: Vector) -> Vector:
    """Convert XYZ to ACEScc."""

    return alg.dot(XYZ_TO_AP1, xyz, dims=alg.D2_D1)


def acescc_to_xyz(acescc: Vector) -> Vector:
    """Convert ACEScc to XYZ."""

    c1 = 2 ** -16
    c2 = (9.72 - 15) / 17.52
    c3 = (math.log2(65504) + 9.72) / 17.52

    acescg = []
    for c in acescc:
        if c <= c2:
            c = (2 ** (c * 17.52 - 9.72) - c1) * 2.0
        elif c2 <= c < c3:
            c = 2 ** (c * 17.52 - 9.72)
        else:
            c = 65504.0
        acescg.append(c)
    return acescg_to_xyz(acescg)


def xyz_to_acescc(xyz: Vector) -> Vector:
    """Convert XYZ to ACEScc."""

    c1 = 2 ** -16
    c2 = 2 ** -15

    acescc = []
    for c in xyz_to_acescg(xyz):
        if c <= 0:
            c = math.log2(c1)
        elif c < c2:
            c = math.log2(c1 + c * 0.5)
        else:
            c = math.log2(c)
        acescc.append((c + 9.72) / 17.52)
    return acescc


def acescct_to_xyz(acescc: Vector) -> Vector:
    """Convert ACEScc to XYZ."""

    c1 = 0.155251141552511
    c2 = 10.5402377416545
    c3 = 0.0729055341958355
    c4 = (math.log2(65504) + 9.72) / 17.52

    acescg = []
    for c in acescc:
        if c <= c1:
            c = (c - c3) / c2
        elif c1 <= c < c4:
            c = 2 ** (c * 17.52 - 9.72)
        else:
            c = 65504
        acescg.append(c)
    return acescg_to_xyz(acescg)


def xyz_to_acescct(xyz: Vector) -> Vector:
    """Convert XYZ to ACEScc."""

    c1 = 0.0078125
    c2 = 10.5402377416545
    c3 = 0.0729055341958355

    acescc = []
    for c in xyz_to_acescg(xyz):
        if c <= c1:
            c = c2 * c + c3
        elif c > c1:
            c = (math.log2(c) + 9.72) / 17.52
        acescc.append(c)
    return acescc


class ACES(SRGB):
    """The ACES color class."""

    BASE = "xyz-d65"
    NAME = "aces"
    SERIALIZE = ("--aces",)  # type: Tuple[str, ...]
    WHITE = (0.32168, 0.33767)

    BOUNDS = (
        GamutBound(MIN, MAX),
        GamutBound(MIN, MAX),
        GamutBound(MIN, MAX)
    )

    @classmethod
    def to_base(cls, coords: Vector) -> Vector:
        """To XYZ."""

        return aces_to_xyz(coords)

    @classmethod
    def from_base(cls, coords: Vector) -> Vector:
        """From XYZ."""

        return xyz_to_aces(coords)


class ACEScg(SRGB):
    """The ACEScg color class."""

    BASE = "xyz-d65"
    NAME = "acescg"
    SERIALIZE = ("--acescg",)  # type: Tuple[str, ...]
    WHITE = (0.32168, 0.33767)

    BOUNDS = (
        GamutBound(CG_MIN, CG_MAX),
        GamutBound(CG_MIN, CG_MAX),
        GamutBound(CG_MIN, CG_MAX)
    )

    @classmethod
    def to_base(cls, coords: Vector) -> Vector:
        """To XYZ."""

        return acescg_to_xyz(coords)

    @classmethod
    def from_base(cls, coords: Vector) -> Vector:
        """From XYZ."""

        return xyz_to_acescg(coords)


class ACEScc(SRGB):
    """The ACEScc color class."""

    BASE = "xyz-d65"
    NAME = "acescc"
    SERIALIZE = ("--acescc",)  # type: Tuple[str, ...]
    WHITE = (0.32168, 0.33767)

    BOUNDS = (
        GamutBound(alg.round_half_up(CC_MIN, 5), alg.round_half_up(CC_MAX, 5)),
        GamutBound(alg.round_half_up(CC_MIN, 5), alg.round_half_up(CC_MAX, 5)),
        GamutBound(alg.round_half_up(CC_MIN, 5), alg.round_half_up(CC_MAX, 5))
    )

    @classmethod
    def to_base(cls, coords: Vector) -> Vector:
        """To XYZ."""

        return acescc_to_xyz(coords)

    @classmethod
    def from_base(cls, coords: Vector) -> Vector:
        """From XYZ."""

        return xyz_to_acescc(coords)


class ACEScct(SRGB):
    """The ACEScct color class."""

    BASE = "xyz-d65"
    NAME = "acescct"
    SERIALIZE = ("--acescct",)  # type: Tuple[str, ...]
    WHITE = (0.32168, 0.33767)

    BOUNDS = (
        GamutBound(alg.round_half_up(CCT_MIN, 5), alg.round_half_up(CCT_MAX, 5)),
        GamutBound(alg.round_half_up(CCT_MIN, 5), alg.round_half_up(CCT_MAX, 5)),
        GamutBound(alg.round_half_up(CCT_MIN, 5), alg.round_half_up(CCT_MAX, 5))
    )

    @classmethod
    def to_base(cls, coords: Vector) -> Vector:
        """To XYZ."""

        return acescct_to_xyz(coords)

    @classmethod
    def from_base(cls, coords: Vector) -> Vector:
        """From XYZ."""

        return xyz_to_acescct(coords)

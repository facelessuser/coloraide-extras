"""
The IgPgTg color space.

https://www.ingentaconnect.com/content/ist/jpi/2020/00000003/00000002/art00002#
"""
from coloraide.spaces import Space, Labish
from coloraide.gamut.bounds import GamutUnbound
from coloraide.cat import WHITES
from coloraide import algebra as alg
from coloraide.types import Vector
from typing import Tuple, cast

XYZ_TO_LMS = [
    [2.968, 2.741, -0.649],
    [1.237, 5.969, -0.173],
    [-0.318, 0.387, 2.311]
]

LMS_TO_XYZ = [
    [0.4343486855574634, -0.20636237011428418, 0.10653033617352772],
    [-0.08785463778363381, 0.20846346647992345, -0.009066845616854866],
    [0.07447971736457795, -0.06330532030466152, 0.44889031421761344]
]

LMS_TO_IGPGTG = [
    [0.117, 1.464, 0.13],
    [8.285, -8.361, 21.4],
    [-1.208, 2.412, -36.53]
]

IGPGTG_TO_LMS = [
    [0.5818464618992484, 0.1233185479390782, 0.07431308420320765],
    [0.6345481937914158, -0.009437923746683553, -0.003270744675229782],
    [0.022656986516578225, -0.0047011518748263665, -0.030048158824914562]
]


def xyz_to_igpgtg(xyz: Vector) -> Vector:
    """XYZ to IgPgTg."""

    lms_in = cast(Vector, alg.dot(XYZ_TO_LMS, xyz, dims=alg.D2_D1))
    lms = [
        alg.npow(lms_in[0] / 18.36, 0.427),
        alg.npow(lms_in[1] / 21.46, 0.427),
        alg.npow(lms_in[2] / 19435, 0.427)
    ]
    return cast(Vector, alg.dot(LMS_TO_IGPGTG, lms, dims=alg.D2_D1))


def igpgtg_to_xyz(itp: Vector) -> Vector:
    """IgPgTg to XYZ."""

    lms = cast(Vector, alg.dot(IGPGTG_TO_LMS, itp, dims=alg.D2_D1))
    lms_in = [
        alg.nth_root(lms[0], 0.427) * 18.36,
        alg.nth_root(lms[1], 0.427) * 21.46,
        alg.nth_root(lms[2], 0.427) * 19435
    ]
    return cast(Vector, alg.dot(LMS_TO_XYZ, lms_in, dims=alg.D2_D1))


class IgPgTg(Labish, Space):
    """The IgPgTg class."""

    BASE = "xyz-d65"
    NAME = "igpgtg"
    SERIALIZE = ("--igpgtg",)  # type: Tuple[str, ...]
    CHANNEL_NAMES = ("ig", "pg", "tg")
    WHITE = WHITES['2deg']['D65']

    BOUNDS = (
        GamutUnbound(0.0, 1.0),
        GamutUnbound(-0.5, 0.5),
        GamutUnbound(-0.5, 0.5)
    )

    @property
    def ig(self) -> float:
        """The `Ig` channel."""

        return self._coords[0]

    @ig.setter
    def ig(self, value: float) -> None:
        """Set `Ig`."""

        self._coords[0] = value

    @property
    def pg(self) -> float:
        """The `Pg` channel."""

        return self._coords[1]

    @pg.setter
    def pg(self, value: float) -> None:
        """Set `Pg`."""

        self._coords[1] = value

    @property
    def tg(self) -> float:
        """The `Tg` channel."""

        return self._coords[2]

    @tg.setter
    def tg(self, value: float) -> None:
        """Set `Tg`."""

        self._coords[2] = value

    @classmethod
    def to_base(cls, coords: Vector) -> Vector:
        """To XYZ."""

        return igpgtg_to_xyz(coords)

    @classmethod
    def from_base(cls, coords: Vector) -> Vector:
        """From XYZ."""

        return xyz_to_igpgtg(coords)

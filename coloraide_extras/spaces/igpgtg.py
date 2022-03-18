"""
The IgPgTg color space.

https://www.ingentaconnect.com/content/ist/jpi/2020/00000003/00000002/art00002#
"""
from coloraide.spaces import Space, Labish, RE_DEFAULT_MATCH, GamutUnbound, WHITES
import re
from coloraide import util
from coloraide.util import MutableVector
from typing import Tuple, cast

XYZ_TO_LMS = [
    [2.968, 2.741, -0.649],
    [1.237, 5.969, -0.173],
    [-0.318, 0.387, 2.311]
]

LMS_TO_XYZ = [
    [0.43434868555746337, -0.20636237011428415, 0.10653033617352774],
    [-0.08785463778363381, 0.20846346647992342, -0.009066845616854866],
    [0.07447971736457795, -0.06330532030466152, 0.44889031421761344]
]

LMS_TO_IGPGTG = [
    [0.117, 1.464, 0.130],
    [8.285, -8.361, 21.40],
    [-1.208, 2.412, -36.53]
]

IGPGTG_TO_LMS = [
    [0.581846461899246, 0.12331854793907822, 0.07431308420320765],
    [0.634548193791416, -0.009437923746683554, -0.003270744675229782],
    [0.02265698651657832, -0.004701151874826367, -0.030048158824914562]
]


def xyz_to_igpgtg(xyz: MutableVector) -> MutableVector:
    """XYZ to IgPgTg."""

    lms_in = cast(MutableVector, util.dot(XYZ_TO_LMS, xyz))
    lms = [
        util.npow(lms_in[0] / 18.36, 0.427),
        util.npow(lms_in[1] / 21.46, 0.427),
        util.npow(lms_in[2] / 19435, 0.427)
    ]
    return cast(MutableVector, util.dot(LMS_TO_IGPGTG, lms))


def igpgtg_to_xyz(itp: MutableVector) -> MutableVector:
    """IgPgTg to XYZ."""

    lms = cast(MutableVector, util.dot(IGPGTG_TO_LMS, itp))
    lms_in = [
        util.nth_root(lms[0], 0.427) * 18.36,
        util.nth_root(lms[1], 0.427) * 21.46,
        util.nth_root(lms[2], 0.427) * 19435
    ]
    return cast(MutableVector, util.dot(LMS_TO_XYZ, lms_in))


class IgPgTg(Labish, Space):
    """The IgPgTg class."""

    BASE = "xyz-d65"
    NAME = "igpgtg"
    SERIALIZE = ("--igpgtg",)  # type: Tuple[str, ...]
    CHANNEL_NAMES = ("ig", "tg", "pg")
    DEFAULT_MATCH = re.compile(RE_DEFAULT_MATCH.format(color_space='|'.join(SERIALIZE), channels=3))
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
    def tg(self) -> float:
        """The `Tg` channel."""

        return self._coords[1]

    @tg.setter
    def tg(self, value: float) -> None:
        """Set `Tg`."""

        self._coords[1] = value

    @property
    def pg(self) -> float:
        """The `Pg` channel."""

        return self._coords[2]

    @pg.setter
    def pg(self, value: float) -> None:
        """Set `Pg`."""

        self._coords[2] = value

    @classmethod
    def to_base(cls, coords: MutableVector) -> MutableVector:
        """To XYZ."""

        return igpgtg_to_xyz(coords)

    @classmethod
    def from_base(cls, coords: MutableVector) -> MutableVector:
        """From XYZ."""

        return xyz_to_igpgtg(coords)

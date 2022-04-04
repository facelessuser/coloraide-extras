"""
The IPT color space.

https://www.researchgate.net/publication/\
221677980_Development_and_Testing_of_a_Color_Space_IPT_with_Improved_Hue_Uniformity.
"""
from coloraide.spaces import Space, Labish
from coloraide.gamut.bounds import GamutUnbound
from coloraide.cat import WHITES
from coloraide import algebra as alg
from coloraide.types import Vector
from typing import Tuple, cast

XYZ_TO_LMS = [
    [0.4001764512951712, 0.7075, -0.08068831054981859],
    [-0.2279865839462744, 1.15, 0.061191135138152386],
    [0.0, 0.0, 0.9182669691320122]
]

LMS_TO_XYZ = [
    [1.8503518239760197, -1.1383686221417688, 0.23844898940542367],
    [0.36683077517134854, 0.6438845448402356, -0.01067344358438],
    [0.0, 0.0, 1.089007917757562]
]

LMS_P_TO_IPT = [
    [0.4, 0.4, 0.2],
    [4.455, -4.851, 0.396],
    [0.8056, 0.3572, -1.1628]
]

IPT_TO_LMS_P = [
    [1.0000000000000004, 0.0975689305146139, 0.2052264331645916],
    [0.9999999999999997, -0.1138764854731471, 0.13321715836999803],
    [1.0, 0.0326151099170664, -0.6768871830691793]
]


def xyz_to_ipt(xyz: Vector) -> Vector:
    """XYZ to IPT."""

    lms_p = [alg.npow(c, 0.43) for c in cast(Vector, alg.dot(XYZ_TO_LMS, xyz, dims=alg.D2_D1))]
    return cast(Vector, alg.dot(LMS_P_TO_IPT, lms_p, dims=alg.D2_D1))


def ipt_to_xyz(ipt: Vector) -> Vector:
    """IPT to XYZ."""

    lms = [alg.nth_root(c, 0.43) for c in cast(Vector, alg.dot(IPT_TO_LMS_P, ipt, dims=alg.D2_D1))]
    return cast(Vector, alg.dot(LMS_TO_XYZ, lms, dims=alg.D2_D1))


class IPT(Labish, Space):
    """The IPT class."""

    BASE = "xyz-d65"
    NAME = "ipt"
    SERIALIZE = ("--ipt",)  # type: Tuple[str, ...]
    CHANNEL_NAMES = ("i", "p", "t")
    WHITE = WHITES['2deg']['D65']

    BOUNDS = (
        GamutUnbound(0.0, 1.0),
        GamutUnbound(-0.5, 0.5),
        GamutUnbound(-0.5, 0.5)
    )

    @property
    def i(self) -> float:
        """The `I` channel."""

        return self._coords[0]

    @i.setter
    def i(self, value: float) -> None:
        """Set `I`."""

        self._coords[0] = value

    @property
    def p(self) -> float:
        """The `P` channel."""

        return self._coords[1]

    @p.setter
    def p(self, value: float) -> None:
        """Set `P`."""

        self._coords[1] = value

    @property
    def t(self) -> float:
        """The `T` channel."""

        return self._coords[2]

    @t.setter
    def t(self, value: float) -> None:
        """Set `T`."""

        self._coords[2] = value

    @classmethod
    def to_base(cls, coords: Vector) -> Vector:
        """To XYZ."""

        return ipt_to_xyz(coords)

    @classmethod
    def from_base(cls, coords: Vector) -> Vector:
        """From XYZ."""

        return xyz_to_ipt(coords)

"""
The IPT color space.

https://www.researchgate.net/publication/\
221677980_Development_and_Testing_of_a_Color_Space_IPT_with_Improved_Hue_Uniformity.
"""
from coloraide.spaces import Space, Labish, RE_DEFAULT_MATCH, GamutUnbound, WHITES
import re
from coloraide import util
from coloraide.util import MutableVector
from typing import Tuple, cast

XYZ_TO_LMS = [
    [0.4001764512951712, 0.7075, -0.08068831054981859],
    [-0.2279865839462744, 1.15, 0.061191135138152386],
    [0.0, 0.0, 0.9182669691320122]
]

LMS_TO_XYZ = [
    [1.8503518239760195, -1.1383686221417688, 0.23844898940542367],
    [0.36683077517134854, 0.6438845448402356, -0.010673443584379994],
    [0.0, 0.0, 1.089007917757562]
]

LMS_TO_IPT = [
    [0.4000, 0.4000, 0.2000],
    [4.4550, -4.851, 0.3960],
    [0.8056, 0.3572, -1.1628]
]

IPT_TO_LMS = [
    [0.9999999999999999, 0.09756893051461393, 0.20522643316459166],
    [0.9999999999999999, -0.11387648547314712, 0.1332171583699981],
    [1.0, 0.0326151099170664, -0.6768871830691793]
]


def xyz_to_ipt(xyz: MutableVector) -> MutableVector:
    """XYZ to IPT."""

    lms_p = [util.npow(c, 0.43) for c in cast(MutableVector, util.dot(XYZ_TO_LMS, xyz))]
    return cast(MutableVector, util.dot(LMS_TO_IPT, lms_p))


def ipt_to_xyz(ipt: MutableVector) -> MutableVector:
    """IPT to XYZ."""

    lms = [util.nth_root(c, 0.43) for c in cast(MutableVector, util.dot(IPT_TO_LMS, ipt))]
    return cast(MutableVector, util.dot(LMS_TO_XYZ, lms))


class IPT(Labish, Space):
    """The IPT class."""

    BASE = "xyz-d65"
    NAME = "ipt"
    SERIALIZE = ("--ipt",)  # type: Tuple[str, ...]
    CHANNEL_NAMES = ("i", "p", "t")
    DEFAULT_MATCH = re.compile(RE_DEFAULT_MATCH.format(color_space='|'.join(SERIALIZE), channels=3))
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

        return self._coords[2]

    @p.setter
    def p(self, value: float) -> None:
        """Set `P`."""

        self._coords[2] = value

    @property
    def t(self) -> float:
        """The `T` channel."""

        return self._coords[1]

    @t.setter
    def t(self, value: float) -> None:
        """Set `T`."""

        self._coords[1] = value

    @classmethod
    def to_base(cls, coords: MutableVector) -> MutableVector:
        """To XYZ."""

        return ipt_to_xyz(coords)

    @classmethod
    def from_base(cls, coords: MutableVector) -> MutableVector:
        """From XYZ."""

        return xyz_to_ipt(coords)

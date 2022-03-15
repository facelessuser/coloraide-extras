"""
The IgTgPg color space.

https://www.ingentaconnect.com/content/ist/jpi/2020/00000003/00000002/art00002#
"""
from coloraide.spaces import Space, Labish, RE_DEFAULT_MATCH, GamutUnbound
import re
from coloraide import util
from coloraide.util import MutableVector
from typing import Tuple, cast

XYZ_TO_LMS = [
    [0.4002, 0.7075, -0.0807],
    [-0.2280, 1.1500, 0.0612],
    [0.0, 0.0, 0.9184]
]

LMS_TO_XYZ = [
    [1.8502429449432054, -1.1383016378672328, 0.23843495850870136],
    [0.36683077517134854, 0.6438845448402355, -0.010673443584379992],
    [0.0, 0.0, 1.088850174216028]
]

LMS_TO_ITP = [
    [0.4000, 0.4000, 0.2000],
    [4.4550, -4.851, 0.3960],
    [0.8056, 0.3572, -1.1628]
]

ITP_TO_LMS = [
    [0.9999999999999999, 0.09756893051461393, 0.20522643316459166],
    [0.9999999999999999, -0.11387648547314712, 0.1332171583699981],
    [1.0, 0.0326151099170664, -0.6768871830691793]
]


def xyz_to_itp(xyz):
    """XYZ to ITP."""

    lms_p = [util.npow(c, 0.43) for c in cast(MutableVector, util.dot(XYZ_TO_LMS, xyz))]
    return cast(MutableVector, util.dot(LMS_TO_ITP, lms_p))


def itp_to_xyz(itp):
    """ITP to XYZ."""

    lms = [util.npow(c, 1 / 0.43) for c in cast(MutableVector, util.dot(ITP_TO_LMS, itp))]
    return cast(MutableVector, util.dot(LMS_TO_XYZ, lms))


class ITP(Labish, Space):
    """The ITP class."""

    BASE = "xyz-d65"
    NAME = "itp"
    SERIALIZE = ("--itp",)  # type: Tuple[str, ...]
    CHANNEL_NAMES = ("i", "t", "p")
    DEFAULT_MATCH = re.compile(RE_DEFAULT_MATCH.format(color_space='|'.join(SERIALIZE), channels=3))
    WHITE = "D65"

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
    def t(self) -> float:
        """The `T` channel."""

        return self._coords[1]

    @t.setter
    def t(self, value: float) -> None:
        """Set `T`."""

        self._coords[1] = value

    @property
    def p(self) -> float:
        """The `P` channel."""

        return self._coords[2]

    @p.setter
    def p(self, value: float) -> None:
        """Set `P`."""

        self._coords[2] = value

    @classmethod
    def to_base(cls, coords: MutableVector) -> MutableVector:
        """To XYZ."""

        return itp_to_xyz(coords)

    @classmethod
    def from_base(cls, coords: MutableVector) -> MutableVector:
        """From XYZ."""

        return xyz_to_itp(coords)

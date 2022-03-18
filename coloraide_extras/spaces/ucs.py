"""
CIE 1960 UCS color class.

http://en.wikipedia.org/wiki/CIE_1960_color_space#Relation_to_CIE_XYZ
"""
from coloraide.spaces import Space, RE_DEFAULT_MATCH, GamutUnbound, WHITES
import re
from coloraide.util import MutableVector
from typing import Tuple


def xyz_to_ucs(xyz: MutableVector) -> MutableVector:
    """Translate XYZ to 1960 UCS."""

    x, y, z = xyz
    return [(2 / 3) * x, y, (-x + 3 * y + z) * 0.5]


def ucs_to_xyz(ucs: MutableVector) -> MutableVector:
    """Translate 1960 UCS to XYZ."""

    u, v, w = ucs
    return [(3 / 2) * u, v, (3 / 2) * u - 3 * v + 2 * w]


class UCS(Space):
    """The 1960 UCS class."""

    BASE = "xyz-d65"
    NAME = "ucs"
    SERIALIZE = ("--ucs",)  # type: Tuple[str, ...]
    CHANNEL_NAMES = ("u", "v", "w")
    DEFAULT_MATCH = re.compile(RE_DEFAULT_MATCH.format(color_space='|'.join(SERIALIZE), channels=3))
    WHITE = WHITES['2deg']['D65']

    BOUNDS = (
        GamutUnbound(0.0, 1.0),
        GamutUnbound(0.0, 1.0),
        GamutUnbound(0.0, 1.0)
    )

    @property
    def u(self) -> float:
        """The u channel."""

        return self._coords[0]

    @u.setter
    def u(self, value: float) -> None:
        """Set u."""

        self._coords[0] = value

    @property
    def v(self) -> float:
        """The v channel."""

        return self._coords[1]

    @v.setter
    def v(self, value: float) -> None:
        """Set v."""

        self._coords[1] = value

    @property
    def w(self) -> float:
        """The w channel."""

        return self._coords[2]

    @w.setter
    def w(self, value: float) -> None:
        """Set w."""

        self._coords[2] = value

    @classmethod
    def to_base(cls, coords: MutableVector) -> MutableVector:
        """To XYZ."""

        return ucs_to_xyz(coords)

    @classmethod
    def from_base(cls, coords: MutableVector) -> MutableVector:
        """From XYZ."""

        return xyz_to_ucs(coords)

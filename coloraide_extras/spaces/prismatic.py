"""
Prismatic color space.

Creates a Maxwell color triangle with a lightness component.

http://psgraphics.blogspot.com/2015/10/prismatic-color-model.html
https://studylib.net/doc/14656976/the-prismatic-color-space-for-rgb-computations
"""
from coloraide.spaces import Space, RE_DEFAULT_MATCH, GamutBound, WHITES
import re
from coloraide.util import MutableVector
from typing import Tuple


def srgb_to_lrgb(rgb: MutableVector) -> MutableVector:
    """Convert sRGB to Prismatic."""

    l = max(rgb)
    s = sum(rgb)
    return [l] + [(c / s) for c in rgb]


def lrgb_to_srgb(lrgb: MutableVector) -> MutableVector:
    """Convert Prismatic to sRGB."""

    rgb = lrgb[1:]
    l = lrgb[0]
    mx = max(rgb)
    return [(l * c) / mx for c in rgb]


class Prismatic(Space):
    """The Prismatic color class."""

    BASE = "srgb"
    NAME = "prismatic"
    SERIALIZE = ("--prismatic",)  # type: Tuple[str, ...]
    CHANNEL_NAMES = ("l", "r", "g", "b")
    CHANNEL_ALIASES = {
        "lightness": 'l',
        "red": 'r',
        "green": 'g',
        "blue": 'b'
    }
    DEFAULT_MATCH = re.compile(RE_DEFAULT_MATCH.format(color_space='|'.join(SERIALIZE), channels=4))
    WHITE = WHITES['2deg']['D65']

    BOUNDS = (
        GamutBound(0.0, 1.0),
        GamutBound(0.0, 1.0),
        GamutBound(0.0, 1.0),
        GamutBound(0.0, 1.0)
    )

    @property
    def l(self) -> float:
        """The lightness channel."""

        return self._coords[0]

    @l.setter
    def l(self, value: float) -> None:
        """Set lightness."""

        self._coords[0] = value

    @property
    def r(self) -> float:
        """The red channel."""

        return self._coords[1]

    @r.setter
    def r(self, value: float) -> None:
        """Set red."""

        self._coords[1] = value

    @property
    def g(self) -> float:
        """The green channel."""

        return self._coords[2]

    @g.setter
    def g(self, value: float) -> None:
        """Set green."""

        self._coords[2] = value

    @property
    def b(self) -> float:
        """Y channel."""

        return self._coords[3]

    @b.setter
    def b(self, value: float) -> None:
        """Set Y."""

        self._coords[3] = value

    @classmethod
    def to_base(cls, coords: MutableVector) -> MutableVector:
        """To sRGB."""

        return lrgb_to_srgb(coords)

    @classmethod
    def from_base(cls, coords: MutableVector) -> MutableVector:
        """From sRGB."""

        return srgb_to_lrgb(coords)

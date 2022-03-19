"""
Uncalibrated, naive CMYK color space.

https://www.w3.org/TR/css-color-5/#cmyk-rgb
"""
from coloraide.spaces import Space, RE_DEFAULT_MATCH, GamutBound, WHITES
import re
from coloraide.util import MutableVector
from typing import Tuple


def srgb_to_cmyk(rgb: MutableVector) -> MutableVector:
    """Convert sRGB to CMYK."""

    k = 1.0 - max(rgb)
    c = m = y = 0.0
    if k != 1:
        r, g, b = rgb
        c = (1.0 - r - k) / (1.0 - k)
        m = (1.0 - g - k) / (1.0 - k)
        y = (1.0 - b - k) / (1.0 - k)

    return [c, m, y, k]


def cmyk_to_srgb(cmyk: MutableVector) -> MutableVector:
    """Convert CMYK to sRGB."""

    c, m, y, k = cmyk
    return [
        1.0 - min(1.0, c * (1.0 - k) + k),
        1.0 - min(1.0, m * (1.0 - k) + k),
        1.0 - min(1.0, y * (1.0 - k) + k)
    ]


class CMYK(Space):
    """The CMYK color class."""

    BASE = "srgb"
    NAME = "cmyk"
    SERIALIZE = ("--cmyk",)  # type: Tuple[str, ...]
    CHANNEL_NAMES = ("c", "m", "y", "k")
    CHANNEL_ALIASES = {
        "cyan": 'c',
        "magenta": 'm',
        "yellow": 'y',
        "black": 'k'
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
    def c(self) -> float:
        """The cyan channel."""

        return self._coords[0]

    @c.setter
    def c(self, value: float) -> None:
        """Set cyan."""

        self._coords[0] = value

    @property
    def m(self) -> float:
        """The magenta channel."""

        return self._coords[1]

    @m.setter
    def m(self, value: float) -> None:
        """Set magenta."""

        self._coords[1] = value

    @property
    def y(self) -> float:
        """The yellow channel."""

        return self._coords[2]

    @y.setter
    def y(self, value: float) -> None:
        """Set yellow."""

        self._coords[2] = value

    @property
    def k(self) -> float:
        """The black channel."""

        return self._coords[3]

    @k.setter
    def k(self, value: float) -> None:
        """Set black."""

        self._coords[3] = value

    @classmethod
    def to_base(cls, coords: MutableVector) -> MutableVector:
        """To sRGB."""

        return cmyk_to_srgb(coords)

    @classmethod
    def from_base(cls, coords: MutableVector) -> MutableVector:
        """From sRGB."""

        return srgb_to_cmyk(coords)

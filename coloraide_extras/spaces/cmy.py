"""Uncalibrated, naive CMY color space."""
from coloraide.spaces import Space
from coloraide.gamut.bounds import GamutBound
from coloraide.cat import WHITES
from coloraide.types import Vector
from typing import Tuple


def srgb_to_cmy(rgb: Vector) -> Vector:
    """Convert sRGB to CMY."""

    return [1 - c for c in rgb]


def cmy_to_srgb(cmy: Vector) -> Vector:
    """Convert CMY to sRGB."""

    return [1 - c for c in cmy]


class CMY(Space):
    """The CMY color class."""

    BASE = "srgb"
    NAME = "cmy"
    SERIALIZE = ("--cmy",)  # type: Tuple[str, ...]
    CHANNEL_NAMES = ("c", "m", "y")
    CHANNEL_ALIASES = {
        "cyan": 'c',
        "magenta": 'm',
        "yellow": 'y'
    }
    WHITE = WHITES['2deg']['D65']

    BOUNDS = (
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

    @classmethod
    def to_base(cls, coords: Vector) -> Vector:
        """To sRGB."""

        return cmy_to_srgb(coords)

    @classmethod
    def from_base(cls, coords: Vector) -> Vector:
        """From sRGB."""

        return srgb_to_cmy(coords)

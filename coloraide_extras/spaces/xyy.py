"""
The xyY color space.

https://en.wikipedia.org/wiki/CIE_1931_color_space#CIE_xy_chromaticity_diagram_and_the_CIE_xyY_color_space
"""
from coloraide.spaces import Space
from coloraide.gamut.bounds import GamutUnbound
from coloraide.cat import WHITES
from coloraide import util
from coloraide.types import Vector
from typing import Tuple


class XyY(Space):
    """The xyY class."""

    BASE = "xyz-d65"
    NAME = "xyy"
    SERIALIZE = ("--xyy",)  # type: Tuple[str, ...]
    CHANNEL_NAMES = ("x", "y", "Y")
    WHITE = WHITES['2deg']['D65']

    BOUNDS = (
        GamutUnbound(0.0, 1.0),
        GamutUnbound(0.0, 1.0),
        GamutUnbound(0.0, 1.0)
    )

    @property
    def x(self) -> float:
        """The x channel."""

        return self._coords[0]

    @x.setter
    def x(self, value: float) -> None:
        """Set x."""

        self._coords[0] = value

    @property
    def y(self) -> float:
        """The y channel."""

        return self._coords[1]

    @y.setter
    def y(self, value: float) -> None:
        """Set y."""

        self._coords[1] = value

    @property
    def Y(self) -> float:
        """Y channel."""

        return self._coords[2]

    @Y.setter
    def Y(self, value: float) -> None:
        """Set Y."""

        self._coords[2] = value

    @classmethod
    def to_base(cls, coords: Vector) -> Vector:
        """To XYZ."""

        return util.xy_to_xyz(coords[0:2], coords[2])

    @classmethod
    def from_base(cls, coords: Vector) -> Vector:
        """From XYZ."""

        return util.xyz_to_xyY(coords, cls.white())

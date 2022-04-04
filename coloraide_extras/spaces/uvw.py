"""
CIE 1964 UVW class.

https://en.wikipedia.org/wiki/CIE_1964_color_space
"""
from coloraide.spaces import Space
from coloraide.gamut.bounds import GamutUnbound
from coloraide.cat import WHITES
from coloraide import util
from coloraide import algebra as alg
from coloraide.types import Vector, VectorLike
from typing import Tuple


def xyz_to_uvw(xyz: Vector, white: VectorLike) -> Vector:
    """
    Translate XYZ to UVW.

    When translating XYZ to the intermediate xyY, we need to treat Y as Y * 100.
    """

    u, v = util.xy_to_uv_1960(util.xyz_to_xyY(xyz, white)[:2])
    u0, v0 = util.xy_to_uv_1960(white)
    w = 25.0 * alg.nth_root(xyz[1] * 100.0, 3) - 17.0
    return [
        13 * w * (u - u0),
        13 * w * (v - v0),
        w
    ]


def uvw_to_xyz(uvw: Vector, white: VectorLike) -> Vector:
    """
    Translate UVW to XYZ.

    When translating xyY back to XYZ, we need to scale Y back as well: Y / 100.
    """

    u0, v0 = util.xy_to_uv_1960(white)
    w = uvw[2]
    x, y = util.uv_1960_to_xy(
        [
            (uvw[0] / (13 * w)) + u0 if w != 0 else u0,
            (uvw[1] / (13 * w)) + v0 if w != 0 else v0
        ]
    )
    return util.xy_to_xyz([x, y], (((w + 17.0) / 25.0) ** 3) / 100.0)


class UVW(Space):
    """The UVW class."""

    BASE = "xyz-d65"
    NAME = "uvw"
    SERIALIZE = ("--uvw",)  # type: Tuple[str, ...]
    CHANNEL_NAMES = ("u", "v", "w")
    WHITE = WHITES['2deg']['D65']

    BOUNDS = (
        GamutUnbound(-0.1, 1.0),
        GamutUnbound(-0.1, 1.0),
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
    def to_base(cls, coords: Vector) -> Vector:
        """To XYZ."""

        return uvw_to_xyz(coords, cls.white())

    @classmethod
    def from_base(cls, coords: Vector) -> Vector:
        """From XYZ."""

        return xyz_to_uvw(coords, cls.white())

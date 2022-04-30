"""
ORGB color space.

https://graphics.stanford.edu/~boulos/papers/orgb_sig.pdf
"""
import math
from coloraide import algebra as alg
from coloraide.spaces import Space, Labish
from coloraide.types import Vector
from coloraide.cat import WHITES
from coloraide.gamut.bounds import GamutBound

RGB_TO_LC1C2 = [
    [0.2990, 0.5870, 0.1140],
    [0.5000, 0.5000, -1.0000],
    [0.8660, -0.8660, 0.0000]
]

LC1C2_TO_RGB = alg.inv(RGB_TO_LC1C2)


def rotate(v: Vector, d: float) -> Vector:
    """Rotate the vector."""

    m = alg.identity(3)
    m[1][1:] = math.cos(d), -math.sin(d)
    m[2][1:] = math.sin(d), math.cos(d)
    return alg.dot(m, v, dims=alg.D2_D1)


def srgb_to_orgb(rgb: Vector) -> Vector:
    """SRGB to ORGB."""

    lcc = alg.dot(RGB_TO_LC1C2, rgb, dims=alg.D2_D1)
    theta = math.atan2(lcc[2], lcc[1])
    theta0 = theta
    atheta = abs(theta)
    if atheta < (math.pi / 3):
        theta0 = (3 / 2) * theta
    elif (math.pi / 3) <= atheta <= math.pi:
        theta0 = math.copysign((math.pi / 2) + (3 / 4) * (atheta - math.pi / 3), theta)

    return rotate(lcc, theta0 - theta)


def orgb_to_srgb(lcc: Vector) -> Vector:
    """ORGB to sRGB."""

    theta0 = math.atan2(lcc[2], lcc[1])
    theta = theta0
    atheta0 = abs(theta0)
    if atheta0 < (math.pi / 2):
        theta = (2 / 3) * theta0
    elif (math.pi / 2) <= atheta0 <= math.pi:
        theta = math.copysign((math.pi / 3) + (4 / 3) * (atheta0 - math.pi / 2), theta0)

    return alg.dot(LC1C2_TO_RGB, rotate(lcc, theta - theta0))


class ORGB(Labish, Space):
    """ORGB color class."""

    BASE = 'srgb'
    NAME = "orgb"
    SERIALIZE = ("--orgb",)
    WHITE = WHITES['2deg']['D65']
    CHANNEL_NAMES = ("l", "cyb", "crg")
    CHANNEL_ALIASES = {
        "luma": "l"
    }
    BOUNDS = (
        GamutBound(0.0, 1.0),
        GamutBound(-1.0, 1.0),
        GamutBound(-1.0, 1.0)
    )

    @property
    def l(self) -> float:
        """The `Luma` channel."""

        return self._coords[0]

    @l.setter
    def l(self, value: float) -> None:
        """Set `Luma`."""

        self._coords[0] = value

    @property
    def cyb(self) -> float:
        """The `Cyb` channel."""

        return self._coords[1]

    @cyb.setter
    def cyb(self, value: float) -> None:
        """Set `Cyb`."""

        self._coords[1] = value

    @property
    def crg(self) -> float:
        """The `Crg` channel."""

        return self._coords[2]

    @crg.setter
    def crg(self, value: float) -> None:
        """Set `Crg`."""

        self._coords[2] = value

    @classmethod
    def to_base(cls, coords: Vector) -> Vector:
        """To base from oRGB."""

        return orgb_to_srgb(coords)

    @classmethod
    def from_base(cls, coords: Vector) -> Vector:
        """From base to oRGB."""

        return srgb_to_orgb(coords)

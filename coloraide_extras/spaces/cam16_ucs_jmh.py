"""
CAM16 UCS JMh (polar).

https://observablehq.com/@jrus/cam16
https://arxiv.org/abs/1802.06067
https://doi.org/10.1002/col.22131
"""
from __future__ import annotations
import math
import bisect
from coloraide.spaces import Space, LChish
from .cam16_ucs import Environment, cam16_to_xyz_d65, xyz_d65_to_cam16
from coloraide.spaces.srgb import lin_srgb
from coloraide.spaces.srgb_linear import lin_srgb_to_xyz
from coloraide.cat import WHITES
from coloraide.channels import Channel, FLG_ANGLE
from coloraide.types import Vector
from typing import Any
from coloraide import algebra as alg

ACHROMATIC_HUE = 209.5429359788321


def xyz_d65_to_cam16_ucs_jmh(xyzd65: Vector, env: Environment) -> Vector:
    """XYZ to CAM16 UCS JMh."""

    cam16 = xyz_d65_to_cam16(xyzd65, env)
    J, M, h = cam16[0], cam16[5], cam16[2]
    M = math.log(1 + env.c2 * M) / env.c2

    return [
        (1 + 100 * env.c1) * J / (1 + env.c1 * J),
        M,
        h
    ]


def cam16_ucs_jmh_to_xyz_d65(ucs: Vector, env: Environment) -> Vector:
    """XYZ to CAM16 UCS JMh."""

    J, M, h = ucs
    M = (math.exp(M * env.c2) - 1) / env.c2
    J = J / (1 - env.c1 * (J - 100))

    return cam16_to_xyz_d65(J=J, M=M, h=h, env=env)


class AchromaTest:
    """
    Test if color is achromatic.

    Should work quite well through the SDR range. Can reasonably handle HDR range out to 3
    which is far enough for anything practical.

    We use a spline mainly to quickly fit the line in a way we do not have to analyze and tune.
    """

    THRESHOLD = 0.06
    MAX_COLORFULNESS = 6.0
    CONVERTER = staticmethod(xyz_d65_to_cam16_ucs_jmh)

    def __init__(self, env: Environment, method: str = 'monotone') -> None:
        """Initialize."""

        # Create a spline that maps the achromatic range for the SDR range
        points = []  # type: list[list[float]]
        self.domain = []  # type: list[float]
        for p in range(25):
            j, m = self.CONVERTER(lin_srgb_to_xyz(lin_srgb([p / 100.0] * 3)), env)[:2]
            self.domain.append(j)
            points.append([j, m])
        for p in range(25, 101, 5):
            j, m = self.CONVERTER(lin_srgb_to_xyz(lin_srgb([p / 55.0] * 3)), env)[:2]
            self.domain.append(j)
            points.append([j, m])
        for p in range(101, 252, 25):
            j, m = self.CONVERTER(lin_srgb_to_xyz(lin_srgb([p / 45.0] * 3)), env)[:2]
            self.domain.append(j)
            points.append([j, m])

        self.spline = alg.interpolate(points, method=method)

    def scale(self, point: float) -> float:
        """Scale the lightness to match the range."""

        if point <= self.domain[0]:
            point = (point - self.domain[0]) / (self.domain[-1] - self.domain[0])
        elif point >= self.domain[-1]:
            point = 1.0 + (point - self.domain[-1]) / (self.domain[-1] - self.domain[0])
        else:
            regions = len(self.domain) - 1
            size = (1 / regions)
            index = 0
            adjusted = 0.0
            index = bisect.bisect(self.domain, point) - 1
            a, b = self.domain[index:index + 2]
            l = b - a
            adjusted = ((point - a) / l) if l else 0.0
            point = size * index + (adjusted * size)
        return point

    def test(self, j: float, m: float) -> bool:
        """Test if the current color is achromatic."""

        # If colorfulness is past this limit, we'd have to have a lightness
        # so high, that our test has already broken down.
        if m > self.MAX_COLORFULNESS:
            return False

        # If we are higher than 1, we are extrapolating;
        # otherwise, use the spline.
        point = self.scale(j)
        if point < 0:  # pragma: no cover
            m2 = 0.0
        else:
            m2 = self.spline(point)[1]
        return m < m2 or abs(m2 - m) < self.THRESHOLD


class CAM16UCSJMh(LChish, Space):
    """CAM16 UCS class."""

    BASE = "xyz-d65"
    NAME = "cam16-ucs-jmh"
    SERIALIZE = ("--cam16-ucs-jmh",)
    CHANNELS = (
        Channel("j", 0.0, 100.0),
        Channel("m", 0, 100.0, limit=(0.0, None)),
        Channel("h", 0.0, 360.0, flags=FLG_ANGLE)
    )
    CHANNEL_ALIASES = {
        "lightness": "j",
        "colorfulness": 'm',
        "hue": 'h'
    }
    WHITE = WHITES['2deg']['D65']
    ENV = Environment('ucs', WHITE, 64 / math.pi * 0.2, 20, 'average', False)

    def __init__(self, **kwargs: Any) -> None:
        """Initialize."""

        super().__init__(**kwargs)

        # Calculate the achromatic line with the given environment
        self.achromatic = AchromaTest(self.ENV)

    def normalize(self, coords: Vector) -> Vector:
        """Normalize the color ensuring no unexpected NaN and achromatic hues are NaN."""

        coords = alg.no_nans(coords)
        j, m = coords[:2]
        if self.achromatic.test(j, m):
            coords[2] = alg.NaN
        return coords

    def to_base(self, coords: Vector) -> Vector:
        """To XYZ from CAM16."""

        j, m = coords[:2]
        if self.achromatic.test(j, m):
            coords[2] = ACHROMATIC_HUE

        return cam16_ucs_jmh_to_xyz_d65(coords, env=self.ENV)

    def from_base(self, coords: Vector) -> Vector:
        """From XYZ to CAM16."""

        jmh = xyz_d65_to_cam16_ucs_jmh(coords, env=self.ENV)
        return self.normalize(jmh)

"""HCT color space."""
from __future__ import annotations
from .cam16_ucs import Environment, cam16_to_xyz_d65, xyz_d65_to_cam16
from coloraide.spaces import Space, LChish
from coloraide.spaces.lab import EPSILON, KAPPA, KE
from coloraide.cat import WHITES
from coloraide.channels import Channel, FLG_ANGLE
from coloraide import algebra as alg
from coloraide.types import Vector, VectorLike
from typing import cast
import math

CHROMA_SCALE = 1 / 2.871588955286716
ACHROMATIC_HUE = 209.5429359788321
POLY_COEF = [2.152855223146154e-07, -7.728527926423952e-05, 0.028943531871995574, 0.5362688035299501]
LOG_COEF1 = [0.1923535302908369, 0.3526144857763279]
LOG_COEF2 = [0.09746113539113359, 0.40076619448389467]


def y_to_lstar(y: float, white: VectorLike) -> float:
    """Convert XYZ Y to Lab L*."""

    y = y / white[1]
    fy = alg.cbrt(y) if y > EPSILON else (KAPPA * y + 16) / 116
    return (116.0 * fy) - 16.0


def lstar_to_y(lstar: float, white: VectorLike) -> float:
    """Convert Lab L* to XYZ Y."""

    fy = (lstar + 16) / 116
    y = fy ** 3 if lstar > KE else lstar / KAPPA
    return y * white[1]


def detect_achromatic(c: float, t: float) -> bool:
    """
    Detect if chroma indicates an achromatic color.

    Normally, with LCh-ish color spaces, a color becomes more achromatic as it
    approaches zero. Many, when you get very close to zero, can safely be
    considered achromatic. HCT (and CAM16 in general) can become achromatic as early
    as 2.8 for chroma, which wouldn't normally be considered close to zero. This is
    response actually increases as lightness increases. So, black it would be zero,
    but at white, it would be ~2.8. The response is mostly linear, but more logarithmic
    near black.

    Luckily, achromatic behavior is fairly easy to predict. Analyzing the behavior,
    we were able to graph the response. Breaking it up into three parts, and fitting
    some curves to the data, we can predict the achromatic using the tone, within
    somewhere around ~+/-0.078 in the tested data. We give it a buffer and use +/- 0.08
    to accommodate any areas that are maybe less precise that we didn't explicitly test.
    """

    if t <= 0:
        c2 = 0.0
    elif t >= 8:
        c2 = POLY_COEF[0] * t ** 3 + POLY_COEF[1] * t ** 2 + POLY_COEF[2] * t + POLY_COEF[3]
    elif t >= 2:
        c2 = max(0.0, LOG_COEF1[0] * math.log(t) + LOG_COEF1[1])
    else:
        c2 = max(0.0, LOG_COEF2[0] * math.log(t) + LOG_COEF2[1])

    return c < c2 or abs(c - c2) < 0.08


def hct_to_xyz(coords: Vector, env: Environment) -> Vector:
    """
    Convert HCT to XYZ.

    Utilize bisect to find the best J that fulfills the current XYZ Y while
    keeping hue and chroma the same (assuming color is not achromatic).
    Not the most efficient, especially if you want to provide the best round
    trip possible. The official Material library that implements HCT, most
    likely has a number of shortcuts to help resolve the color faster, some
    may come at the cost of precision. Worth looking into in the future.
    """

    # Threshold of how close is close enough
    # Precision requires more iterations...maybe too many :)
    threshold = 0.000000002

    h, c, t = coords[:]

    # If we are achromatic, make sure to set the hue such that the algorithm
    # will get us back to the right achromatic color. The hue is ~209.5.
    if detect_achromatic(c, t):
        h = ACHROMATIC_HUE

    # No NaN
    if alg.is_nan(h):  # pragma: no cover
        h = 0

    # Initialize J with our T, set our bisect bounds,
    # and get our target XYZ Y from T
    y = lstar_to_y(t, env.ref_white)
    low, high, j = 0.0, 100.0, t

    # Try to find a J such that the returned y matches the returned y of the L*
    while (high - low) > threshold:
        xyz = cam16_to_xyz_d65(J=j, C=c, h=h, env=env)

        delta = xyz[1] - y

        # We are within range, so return XYZ
        if abs(delta) <= threshold:
            return xyz

        if delta < 0:
            low = j
        else:
            high = j

        j = (high + low) * 0.5

    # Return the best that we have
    return cam16_to_xyz_d65(J=j, C=coords[1], h=coords[0], env=env)  # pragma: no cover


def xyz_to_hct(coords: Vector, env: Environment) -> Vector:
    """Convert XYZ to HCT."""

    cam16 = xyz_d65_to_cam16(coords, env)
    t = y_to_lstar(coords[1], env.ref_white)
    c, h = cam16[1:3]

    # If we are achromatic, set the hue as such.
    if detect_achromatic(c, t):
        h = alg.NaN

    return [h, c, alg.clamp(t, 0.0, 100.0)]


class HCT(LChish, Space):
    """CAM16 UCS class."""

    BASE = "xyz-d65"
    NAME = "hct"
    SERIALIZE = ("--hct",)
    CHANNELS = (
        Channel("h", 0.0, 360.0, flags=FLG_ANGLE),
        Channel("c", 0.0, 145.0, limit=(0.0, None)),
        Channel("t", 0.0, 100.0, limit=(0.0, 100.0))
    )
    CHANNEL_ALIASES = {
        "lightness": "t",
        "tone": "t",
        "chroma": "c",
        "hue": "h"
    }
    WHITE = WHITES['2deg']['D65']
    ENV = Environment('ucs', WHITE, 11.725677948856951, 0.18418651851244416 * 100, 'average', False)

    def normalize(self, coords: Vector) -> Vector:
        """Normalize the color ensuring no unexpected NaN and achromatic hues are NaN."""

        coords = alg.no_nans(coords)
        c, t = coords[1:-1]
        if detect_achromatic(c, t):
            coords[0] = alg.NaN
        return coords

    def lchish_names(self) -> tuple[str, ...]:
        """Return LCh-ish names in the order L C h."""

        channels = cast(Space, self).channels
        return channels[2], channels[1], channels[0]

    @classmethod
    def to_base(cls, coords: Vector) -> Vector:
        """To XYZ from HCT."""

        return hct_to_xyz(coords, cls.ENV)

    @classmethod
    def from_base(cls, coords: Vector) -> Vector:
        """From XYZ to HCT."""

        return xyz_to_hct(coords, cls.ENV)

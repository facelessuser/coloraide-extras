"""
HCT color space.

This implements the HCT color space as described. This is not a port of the Material library.
We simply, as described, create a color space with CIELAB L* and CAM16's C and h components.
Environment settings are calculated with the assumption of L* 50.

Our approach getting back to sRGB is likely different as we are using a simple binary search
to help calculate the missing piece (J) needed to convert CAM16 C and h back to XYZ such that
Y matches the L* conversion back to Y. I am certain the Material library is most likely
employing further tricks to resolve faster. We also try to get as good round trip as possible,
which forces us to probably make more iterations than Material does (none of this as been confirmed).

As ColorAide usually cares about setting powerless hues as NaN, especially for good interpolation,
we've also calculated the cut off for chromatic colors and will properly enforce achromatic,powerless
hues. This is because CAM16 actually resolves colors as achromatic before chroma reaches zero as
lightness increases. In the SDR range, a Tone of 100 will have a cut off as high as ~2.87 chroma.

Generally, the HCT color space is restricted to SDR range. lightness above this range will be clamped.
This is required in order for us to properly gauge and search for the appropriate CAM16 J when
converting back to other SDR color spaces. We do not clamp chroma's maximum, but we will clamp minimum
to zero. This allows HCT to work with Display P3 and other SDR RGB spaces.

Though we did not port HCT from Material Color Utilities, we did test against it, and are pretty
much on point. The only differences are due to matrix precision and white point precision. Material
uses an RGB <-> XYZ matrix that rounds values off significantly more than we do. Also, while we
calculate the XYZ points from the `xy` points without rounding, they have rounded XYZ points. All of
this just makes it so that after about 2 decimal points, things can differ some:

Material:

```
> hct.Hct.fromInt(0xff305077)
Hct {
  argb: 4281356407,
  internalHue: 256.8040416857594,
  internalChroma: 31.761442797741243,
  internalTone: 33.34501410942328
}
```

ColorAide:

```
>>> from coloraide_extras.everything import ColorAll as Color
>>> Color('#305077').convert('hct')
color(--hct 256.79 31.766 33.344 / 1)
```

Differences are inconsequential.
"""
from __future__ import annotations
from .cam16_ucs import Environment, cam16_to_xyz_d65, xyz_d65_to_cam16
from .cam16_ucs_jmh import AchromaTest, ACHROMATIC_HUE
from coloraide.spaces.srgb import lin_srgb
from coloraide.spaces.srgb_linear import lin_srgb_to_xyz
from coloraide.spaces import Space, LChish
from coloraide.spaces.lab import EPSILON, KAPPA, KE
from coloraide.cat import WHITES
from coloraide.channels import Channel, FLG_ANGLE
from coloraide import algebra as alg
from coloraide.types import Vector, VectorLike
from typing import Any, cast
from coloraide import util
import math


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

    # No NaN
    if alg.is_nan(h):  # pragma: no cover
        h = 0

    if t == 0:
        return [0.0, 0.0, 0.0]
    elif t == 100.0:
        return env.ref_white[:]

    # Initialize J with our T, set our bisect bounds,
    # and get our target XYZ Y from T
    j = t
    low = 0.0
    high = 100.0 if t <= 100.0 else 1000.0  # SDR or HDR
    y = lstar_to_y(t, env.ref_white)

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

    return [h, c, alg.clamp(t, 0.0)]


class HCTAchromaTest(AchromaTest):
    """
    Test HCT achromatic response.

    This replaces are first approximation below and does just about as well. We use the spline
    approach to consolidate approaches with CAM16 UCS JMh. For others, below is much easier to
    implement if you don't already have access to a spline implementation.

    ```
    POLY_COEF = [2.152855223146154e-07, -7.728527926423952e-05, 0.028943531871995574, 0.5362688035299501]
    LOG_COEF1 = [0.1923535302908369, 0.3526144857763279]
    LOG_COEF2 = [0.09746113539113359, 0.40076619448389467]

    if t <= 0:
        c2 = 0.0
    elif t >= 8:
        c2 = POLY_COEF[0] * t ** 3 + POLY_COEF[1] * t ** 2 + POLY_COEF[2] * t + POLY_COEF[3]
    elif t >= 2:
        c2 = LOG_COEF1[0] * math.log(t) + LOG_COEF1[1]
    else:
        # Very small tone may produce a small negative value, ensure we don't return such a value.
        c2 = max(0.0, LOG_COEF2[0] * math.log(t) + LOG_COEF2[1])
    ```
    """

    CONVERTER = staticmethod(xyz_to_hct)
    THRESHOLD = 0.085
    MAX_COLORFULNESS = 7.5

    def __init__(self, env: Environment, method: str = 'natural') -> None:
        """Initialize."""

        # Create a spline that maps the achromatic range for the SDR range
        points = []  # type: list[list[float]]
        self.domain = []  # type: list[float]
        # We need higher resolution in this first bend.
        for p in range(51):
            m, j = self.CONVERTER(lin_srgb_to_xyz(lin_srgb([p / 200.0] * 3)), env)[1:]
            self.domain.append(j)
            points.append([j, m])
        # This is fairly straight, so about 10 points should do.
        for p in range(50, 101, 5):
            m, j = self.CONVERTER(lin_srgb_to_xyz(lin_srgb([p / 100.0] * 3)), env)[1:]
            self.domain.append(j)
            points.append([j, m])
        for p in range(101, 502, 25):
            m, j = self.CONVERTER(lin_srgb_to_xyz(lin_srgb([p / 75.0] * 3)), env)[1:]
            self.domain.append(j)
            points.append([j, m])

        self.spline = alg.interpolate(points, method=method)


class HCT(LChish, Space):
    """HCT class."""

    BASE = "xyz-d65"
    NAME = "hct"
    SERIALIZE = ("--hct",)
    CHANNELS = (
        Channel("h", 0.0, 360.0, flags=FLG_ANGLE),
        Channel("c", 0.0, 145.0, limit=(0.0, None)),
        Channel("t", 0.0, 100.0, limit=(0.0, None))
    )
    CHANNEL_ALIASES = {
        "lightness": "t",
        "tone": "t",
        "chroma": "c",
        "hue": "h"
    }
    WHITE = WHITES['2deg']['D65']
    Y_LSTAR_50 = lstar_to_y(50.0, util.xy_to_xyz(WHITE))
    ENV = Environment(
        'ucs',
        WHITE,
        200 / math.pi * Y_LSTAR_50,
        Y_LSTAR_50 * 100,
        'average',
        False
    )

    def __init__(self, **kwargs: Any) -> None:
        """Initialize."""

        super().__init__(**kwargs)

        # Calculate the achromatic line with the given environment
        self.achromatic = HCTAchromaTest(self.ENV)

    def normalize(self, coords: Vector) -> Vector:
        """Normalize the color ensuring no unexpected NaN and achromatic hues are NaN."""

        coords = alg.no_nans(coords)
        m, j = coords[1:3]
        if self.achromatic.test(j, m):
            coords[0] = alg.NaN
        return coords

    def lchish_names(self) -> tuple[str, ...]:
        """Return LCh-ish names in the order L C h."""

        channels = cast(Space, self).channels
        return channels[2], channels[1], channels[0]

    def to_base(self, coords: Vector) -> Vector:
        """To XYZ from HCT."""

        m, j = coords[1:3]
        if self.achromatic.test(j, m):
            coords[0] = ACHROMATIC_HUE

        return hct_to_xyz(coords, self.ENV)

    def from_base(self, coords: Vector) -> Vector:
        """From XYZ to HCT."""

        hct = xyz_to_hct(coords, self.ENV)
        return self.normalize(hct)

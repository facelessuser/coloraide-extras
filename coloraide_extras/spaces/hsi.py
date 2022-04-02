"""
HSI class.

https://en.wikipedia.org/wiki/HSL_and_HSV#Saturation
"""
from coloraide.spaces import Space, FLG_ANGLE, FLG_OPT_PERCENT, GamutBound, Cylindrical, WHITES
from coloraide import algebra as alg
from coloraide import util
from coloraide.types import MutableVector
from typing import Tuple


def srgb_to_hsi(rgb: MutableVector) -> MutableVector:
    """SRGB to HSI."""

    r, g, b = rgb
    h = alg.NaN
    s = 0.0
    mx = max(rgb)
    mn = min(rgb)
    i = sum(rgb) * 1 / 3
    s = 0 if i == 0 else 1 - (mn / i)
    c = mx - mn

    if c != 0.0:
        if mx == r:
            h = (g - b) / c
        elif mx == g:
            h = (b - r) / c + 2.0
        else:
            h = (r - g) / c + 4.0
        h *= 60.0

    return [util.constrain_hue(h), s, i]


def hsi_to_srgb(hsi: MutableVector) -> MutableVector:
    """HSI to RGB."""

    h, s, i = hsi
    h = h % 360
    h /= 60
    z = 1 - abs(h % 2 - 1)
    c = (3 * i * s) / (1 + z)
    x = c * z

    if alg.is_nan(h):  # pragma: no cover
        # In our current setup, this will not occur. If colors are naturally achromatic,
        # they will resolve to zeros automatically even without this check. This case
        # would be a shortcut normally.
        #
        # Unnatural cases, such as explicitly setting of hue to undefined, could cause this,
        # but the conversion pipeline converts all undefined values to zero. We'd have to
        # encounter a natural case due to conversion to or from HSI mid pipeline to trigger
        # this, and we are not currently in a position where that would occur with sRGB being
        # the only pass-through.
        rgb = [0.0] * 3
    elif 0 <= h <= 1:
        rgb = [c, x, 0]
    elif 1 <= h <= 2:
        rgb = [x, c, 0]
    elif 2 <= h <= 3:
        rgb = [0, c, x]
    elif 3 <= h <= 4:
        rgb = [0, x, c]
    elif 4 <= h <= 5:
        rgb = [x, 0, c]
    else:
        rgb = [c, 0, x]
    m = i * (1 - s)

    return [chan + m for chan in rgb]


class HSI(Cylindrical, Space):
    """HSI class."""

    BASE = "srgb"
    NAME = "hsi"
    SERIALIZE = ("--hsi",)
    CHANNEL_NAMES = ("h", "s", "i")
    CHANNEL_ALIASES = {
        "hue": "h",
        "saturation": "s",
        "intensity": "i"
    }
    WHITE = WHITES['2deg']['D65']
    GAMUT_CHECK = "srgb"

    BOUNDS = (
        GamutBound(0.0, 360.0, FLG_ANGLE),
        GamutBound(0.0, 1.0, FLG_OPT_PERCENT),
        GamutBound(0.0, 1.0, FLG_OPT_PERCENT)
    )

    @property
    def h(self) -> float:
        """Hue channel."""

        return self._coords[0]

    @h.setter
    def h(self, value: float) -> None:
        """Shift the hue."""

        self._coords[0] = value

    @property
    def s(self) -> float:
        """Saturation channel."""

        return self._coords[1]

    @s.setter
    def s(self, value: float) -> None:
        """Set saturation."""

        self._coords[1] = value

    @property
    def i(self) -> float:
        """Intensity channel."""

        return self._coords[2]

    @i.setter
    def i(self, value: float) -> None:
        """Set intensity channel."""

        self._coords[2] = value

    @classmethod
    def null_adjust(cls, coords: MutableVector, alpha: float) -> Tuple[MutableVector, float]:
        """On color update."""

        h, s, i = alg.no_nans(coords)
        h = h % 360
        h /= 60
        z = 1 - abs(h % 2 - 1)
        c = (3 * i * s) / (1 + z)

        if c == 0:
            coords[0] = alg.NaN

        return coords, alg.no_nan(alpha)

    @classmethod
    def to_base(cls, coords: MutableVector) -> MutableVector:
        """To sRGB from HSI."""

        return hsi_to_srgb(coords)

    @classmethod
    def from_base(cls, coords: MutableVector) -> MutableVector:
        """From sRGB to HSI."""

        return srgb_to_hsi(coords)

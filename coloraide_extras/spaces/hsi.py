"""HSI class."""
from coloraide.spaces import Space, RE_DEFAULT_MATCH, FLG_ANGLE, FLG_OPT_PERCENT, GamutBound, Cylindrical, WHITES
from coloraide import util
import re
from coloraide.util import MutableVector
from typing import Tuple


def srgb_to_hsi(rgb: MutableVector) -> MutableVector:
    """SRGB to HSI."""

    r, g, b = rgb
    h = util.NaN
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
    """
    HSI to RGB.

    https://en.wikipedia.org/wiki/HSL_and_HSV#Saturation
    """

    h, s, i = hsi
    h = h % 360
    h /= 60
    z = 1 - abs(h % 2 - 1)
    c = (3 * i * s) / (1 + z)
    x = c * z

    if util.is_nan(h):
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
    DEFAULT_MATCH = re.compile(RE_DEFAULT_MATCH.format(color_space='|'.join(SERIALIZE), channels=3))
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

        if coords[2] == 0:
            coords[0] = util.NaN

        return coords, alpha

    @classmethod
    def to_base(cls, coords: MutableVector) -> MutableVector:
        """To sRGB from HSI."""

        return hsi_to_srgb(coords)

    @classmethod
    def from_base(cls, coords: MutableVector) -> MutableVector:
        """From sRGB to HSI."""

        return srgb_to_hsi(coords)

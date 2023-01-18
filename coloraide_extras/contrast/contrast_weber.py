"""
Weber color contrast.

https://en.wikipedia.org/wiki/Contrast_(vision)#Weber_contrast.
"""
from __future__ import annotations
from coloraide.contrast import ColorContrast
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from coloraide import Color

MAX = 50000


class ContrastWeber(ColorContrast):
    """Weber contrast."""

    NAME = "weber"

    @classmethod
    def contrast(cls, color1: Color, color2: Color, **kwargs: Any) -> float:
        """Contrast."""

        lum1 = max(color1.luminance(), 0.0)
        lum2 = max(color2.luminance(), 0.0)

        if lum1 > lum2:
            lum2, lum1 = lum1, lum2

        if lum1 == 0:
            return MAX

        return (lum2 - lum1) / lum1

"""
Michelson color contrast.

https://en.wikipedia.org/wiki/Contrast_(vision)#Michelson_contrast.
"""
from __future__ import annotations
from coloraide.contrast import ColorContrast
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from coloraide import Color


class ContrastMichelson(ColorContrast):
    """Michelson contrast."""

    NAME = "michelson"

    @classmethod
    def contrast(cls, color1: Color, color2: Color, **kwargs: Any) -> float:
        """Contrast."""

        lum1 = max(color1.luminance(), 0.0)
        lum2 = max(color2.luminance(), 0.0)

        if lum1 > lum2:
            lum2, lum1 = lum1, lum2

        d = lum2 + lum1

        if d == 0:
            return 0

        return (lum2 - lum1) / d

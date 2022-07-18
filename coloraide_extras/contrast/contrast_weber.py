"""
Weber color contrast.

https://en.wikipedia.org/wiki/Contrast_(vision)#Weber_contrast.
"""
from coloraide.contrast import ColorContrast
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from coloraide import Color


class ContrastWeber(ColorContrast):
    """Weber contrast."""

    NAME = "weber"

    @classmethod
    def contrast(cls, color1: 'Color', color2: 'Color', **kwargs: Any) -> float:
        """Contrast."""

        lum1 = color1.luminance()
        lum2 = color2.luminance()

        if lum1 > lum2:
            lum2, lum1 = lum1, lum2

        if lum1 == 0:
            return 0

        return (lum2 - lum1) / lum1

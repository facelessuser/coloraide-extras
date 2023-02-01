"""
L* color contrast.

Used for color contrast in Google's HCT.

https://material.io/blog/science-of-color-design
"""
from __future__ import annotations
from coloraide.contrast import ColorContrast
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from coloraide import Color


class ContrastLstar(ColorContrast):
    """L* contrast."""

    NAME = "lstar"

    @classmethod
    def contrast(cls, color1: Color, color2: Color, **kwargs: Any) -> float:
        """Contrast."""

        l1 = color1.get('lch-d65.lightness')
        l2 = color2.get('lch-d65.lightness')

        if l1 > l2:
            l2, l1 = l1, l2

        return l2 - l1
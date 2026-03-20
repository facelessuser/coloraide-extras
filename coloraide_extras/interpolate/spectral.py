"""
Spectral mixing.

See source in ColorAide.
"""
from __future__ import annotations
import warnings
from coloraide.interpolate.spectral import Spectral, SpectralContinuous
from typing import Any

__all__ = ('Spectral', 'SpectralContinuous')

__deprecated__ = {
    "Spectral": ("coloraide.interpolate.spectral.Spectral", Spectral),
    "SpectralContinuous": ("coloraide.interpolate.spectral.SpectralContinuous", SpectralContinuous)
}


def __getattr__(name: str) -> Any:
    """Get attribute."""

    deprecated = __deprecated__.get(name)
    if deprecated:
        warnings.warn(
            f"'{name}' are deprecated as they are now included ColorAide directly. Use '{deprecated[0]}' instead.",
            category=DeprecationWarning,
            stacklevel=4
        )
        return deprecated[1]
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

"""Everything but the kitchen sink."""
from __future__ import annotations
from coloraide.everything import ColorAll as Base
from coloraide import stop, hint, NaN
from .spaces.ucs import UCS
from .spaces.uvw import UVW
from .contrast.contrast_weber import ContrastWeber
from .contrast.contrast_michelson import ContrastMichelson

__all__ = ("ColorAll", 'NaN', 'stop', 'hint')


class ColorAll(Base):
    """Color class containing all defaults and extra color spaces."""


# If we get out of sync with ColorAide, we may try
# and overwrite a package that used to be here, but
# is now hosted there.
ColorAll.register(
    [
        # Spaces
        UCS(),
        UVW(),

        # Delta E

        # Contrast
        ContrastWeber(),
        ContrastMichelson()

        # Gamut
    ],
    silent=True
)

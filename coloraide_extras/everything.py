"""Everything but the kitchen sink."""
from __future__ import annotations
from coloraide.everything import ColorAll as Base
from coloraide import stop, hint, NaN
from .spaces.ucs import UCS
from .spaces.uvw import UVW
from .spaces.cam16_ucs import CAM16UCS, CAM16SCD, CAM16LCD
from .spaces.cam16_ucs_jmh import CAM16UCSJMh
from .spaces.hct import HCT
from .distance.delta_e_cam16 import DECAM16
from .distance.delta_e_hct import DEHCT
from .contrast.contrast_weber import ContrastWeber
from .contrast.contrast_michelson import ContrastMichelson
from .contrast.contrast_lstar import ContrastLstar
from .gamut.fit_hct_chroma import HCTChroma

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
        HCT(),
        CAM16UCS(),
        CAM16SCD(),
        CAM16LCD(),
        CAM16UCSJMh(),

        # Delta E
        DECAM16(),
        DEHCT(),

        # Contrast
        ContrastWeber(),
        ContrastMichelson(),
        ContrastLstar(),

        # Gamut
        HCTChroma()
    ],
    silent=True
)

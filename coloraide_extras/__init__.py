"""ColorAide Extra."""
from .__meta__ import __version_info__, __version__  # noqa: F401
from coloraide import stop, hint, NaN
from coloraide import ColorAll as Base
from coloraide.types import Plugin
from .spaces.ucs import UCS
from .spaces.uvw import UVW
from .spaces.cam16_ucs import CAM16UCS, CAM16SCD, CAM16LCD
from .distance.delta_e_cam16 import DECAM16
from .contrast.contrast_weber import ContrastWeber
from .contrast.contrast_michelson import ContrastMichelson
from typing import List, Type

__all__ = ("Color", "SPACES", 'NaN', 'stop', 'hint')

SPACES = [UCS, UVW, CAM16UCS, CAM16SCD, CAM16LCD]  # type: List[Type[Plugin]]

DE = [DECAM16]  # type: List[Type[Plugin]]

CONTRAST = [ContrastWeber, ContrastMichelson]  # type: List[Type[Plugin]]


class Color(Base):
    """Color class containing all default and extra color spaces."""


# If we get out of sync with ColorAide, we may try
# and overwrite a package that used to be here, but
# is now hosted there.
Color.register(SPACES + DE + CONTRAST, silent=True)

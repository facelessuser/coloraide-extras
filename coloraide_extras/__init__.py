"""ColorAide Extra."""
from .__meta__ import __version_info__, __version__  # noqa: F401
from coloraide import stop, hint, NaN
from coloraide import ColorAll as Base
from .spaces.ucs import UCS
from .spaces.uvw import UVW

__all__ = ("Color", "SPACES", 'NaN', 'stop', 'hint')

SPACES = [UCS, UVW]


class Color(Base):
    """Color class containing all default and extra color spaces."""


# If we get out of sync with ColorAide, we may try
# and overwrite a package that used to be here, but
# is now hosted there.
Color.register(SPACES, silent=True)

"""ColorAide Extra."""
from .__meta__ import __version_info__, __version__  # noqa: F401
from coloraide import NaN
from coloraide.interpolate import Piecewise, Lerp
from coloraide import Color as Base
from .spaces.hsi import HSI
from .spaces.ipt import IPT
from .spaces.igpgtg import IgPgTg
from .spaces.cmy import CMY
from .spaces.cmyk import CMYK
from .spaces.ucs import UCS
from .spaces.uvw import UVW
from .spaces.xyy import XyY
from .spaces.hunter_lab import HunterLab
from .spaces.prismatic import Prismatic
from .spaces.rlab import RLAB
from .spaces.orgb import ORGB
from .spaces.aces import ACES, ACEScg, ACEScc, ACEScct

__all__ = ("Color", "SPACES", 'NaN', 'Piecewise', 'Lerp')

SPACES = [HSI, IPT, IgPgTg, CMY, CMYK, UCS, UVW, XyY, HunterLab, Prismatic, RLAB, ORGB, ACES, ACEScg, ACEScc, ACEScct]


class Color(Base):
    """Color class containing all default and extra color spaces."""


Color.register(SPACES)

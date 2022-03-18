"""ColorAide Extra."""
from .__meta__ import __version_info__, __version__  # noqa: F401
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

__all__ = ("Color", "SPACES")

SPACES = [HSI, IPT, IgPgTg, CMY, CMYK, UCS, UVW, XyY, HunterLab, Prismatic]


class Color(Base):
    """Color class containing all default and extra color spaces."""


Color.register(SPACES)

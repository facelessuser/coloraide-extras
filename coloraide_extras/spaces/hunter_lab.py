"""
Hunter Lab class.

https://support.hunterlab.com/hc/en-us/articles/203997095-Hunter-Lab-Color-Scale-an08-96a2
"""
from coloraide.spaces import RE_DEFAULT_MATCH, WHITES
from coloraide.spaces.lab import Lab
from coloraide import util
import re
from coloraide.util import MutableVector
from typing import cast

# Values for the original Hunter Lab with illuminant C.
# Also, the original calculated `ka` and `kb` under illuminant C.
# Original values:
#   https://support.hunterlab.com/hc/en-us/articles/203997095-Hunter-Lab-Color-Scale-an08-96a2
# Slightly more precise values in `rdab`:
#   https://hunterlabdotcom.files.wordpress.com/2012/07/an-1016-hunter-rd-a-b-color-scale-update-12-07-03.pdf
CXN = 98.043
CYN = 100.0
CZN = 118.106
CKA = 175.0
CKB = 70.0
# Conversion factors
CKA_FACTOR = CKA / (CXN + CYN)
CKB_FACTOR = CKB / (CZN + CYN)


def xyz_to_hlab(xyz: MutableVector, white: MutableVector) -> MutableVector:
    """Convert XYZ to Hunter Lab."""

    xn, yn, zn = cast(MutableVector, util.multiply(util.xy_to_xyz(white), 100))
    ka = CKA_FACTOR * (xn + yn)
    kb = CKB_FACTOR * (yn + zn)
    x, y, z = cast(MutableVector, util.multiply(xyz, 100))
    l = util.nth_root(y / yn, 2)
    a = b = 0
    if l != 0:
        a = ka * (x / xn - y / yn) / l
        b = kb * (y / yn - z / zn) / l
    return [l * 100, a, b]


def hlab_to_xyz(hlab: MutableVector, white: MutableVector) -> MutableVector:
    """Convert Hunter Lab to XYZ."""

    xn, yn, zn = cast(MutableVector, util.multiply(util.xy_to_xyz(white), 100))
    ka = CKA_FACTOR * (xn + yn)
    kb = CKB_FACTOR * (yn + zn)
    l, a, b = hlab
    l /= 100
    y = (l ** 2) * yn
    x = (((a * l) / ka) + (y / yn)) * xn
    z = (((b * l) / kb) - (y / yn)) * -zn
    return cast(MutableVector, util.divide([x, y, z], 100))


class HunterLab(Lab):
    """Hunter Lab class."""

    BASE = 'xyz-d65'
    NAME = "hunter-lab"
    SERIALIZE = ("--hunter-lab",)
    DEFAULT_MATCH = re.compile(RE_DEFAULT_MATCH.format(color_space='|'.join(SERIALIZE), channels=3))
    WHITE = WHITES['2deg']['D65']

    @classmethod
    def to_base(cls, coords: MutableVector) -> MutableVector:
        """To XYZ from Hunter Lab."""

        return hlab_to_xyz(coords, cls.white())

    @classmethod
    def from_base(cls, coords: MutableVector) -> MutableVector:
        """From XYZ to Hunter Lab."""

        return xyz_to_hlab(coords, cls.white())

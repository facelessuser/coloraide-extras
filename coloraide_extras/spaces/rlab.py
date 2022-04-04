"""
RLAB.

https://scholarworks.rit.edu/cgi/viewcontent.cgi?article=1153&context=article
https://www.imaging.org/site/PDFS/Papers/1997/RP-0-67/2368.pdf
"""
from coloraide.cat import WHITES
from coloraide.spaces.lab import Lab
from coloraide import algebra as alg
from coloraide.types import MutableVector
from typing import cast

XYZ_TO_XYZ_REF = [
    [1.0521266389510715, 2.220446049250313e-16, 0.0],
    [0.0, 1.0, 2.414043899674756e-19],
    [0.0, 0.0, 0.9182249511582473]
]

XYZ_REF_TO_XYZ = [
    [0.9504559270516716, -2.110436108208428e-16, 5.548406636355788e-35],
    [0.0, 1.0, -2.629033219615395e-19],
    [0.0, 0.0, 1.0890577507598784]
]

EXP = 2.3


def rlab_to_xyz(rlab: MutableVector) -> MutableVector:
    """RLAB to XYZ."""

    l, a, b = rlab
    yr = l / 100
    xr = alg.npow((a / 430) + yr, EXP)
    zr = alg.npow(yr - (b / 170), EXP)
    return cast(MutableVector, alg.dot(XYZ_REF_TO_XYZ, [xr, alg.npow(yr, EXP), zr]))


def xyz_to_rlab(xyz: MutableVector) -> MutableVector:
    """XYZ to RLAB."""

    xyz_ref = cast(MutableVector, alg.dot(XYZ_TO_XYZ_REF, xyz))
    xr, yr, zr = [alg.nth_root(c, EXP) for c in xyz_ref]
    l = 100 * yr
    a = 430 * (xr - yr)
    b = 170 * (yr - zr)
    return [l, a, b]


class RLAB(Lab):
    """RLAB class."""

    BASE = 'xyz-d65'
    NAME = "rlab"
    SERIALIZE = ("--rlab",)
    WHITE = WHITES['2deg']['D65']

    @classmethod
    def to_base(cls, coords: MutableVector) -> MutableVector:
        """To XYZ from Hunter Lab."""

        return rlab_to_xyz(coords)

    @classmethod
    def from_base(cls, coords: MutableVector) -> MutableVector:
        """From XYZ to Hunter Lab."""

        return xyz_to_rlab(coords)
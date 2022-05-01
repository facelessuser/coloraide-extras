"""
Hunter Lab class.

https://support.hunterlab.com/hc/en-us/articles/203997095-Hunter-Lab-Color-Scale-an08-96a2
"""
from coloraide.cat import WHITES
from coloraide.spaces.lab import Lab
from coloraide import algebra as alg
from coloraide import util
from coloraide.types import Vector, VectorLike

# Values for the original Hunter Lab with illuminant C.
# Also, the original calculated `ka` and `kb` under illuminant C.
# Original values:
#   https://support.hunterlab.com/hc/en-us/articles/203997095-Hunter-Lab-Color-Scale-an08-96a2
CXN = 98.04
CYN = 100.0
CZN = 118.11
CKA = 175.0
CKB = 70.0

# We will calculate our adapted `ka`, `kb` directly as our D65 white point isn't exactly the same.
# This also allows us to change the white point to anything, and it should still work.
#      | `Xn`               | `Yn`               | `Ka`                | `Kb`
# ---- | -------------------| ------------------ | ------------------- | ----
# Spec | 95.02              | 108.82             | 172.30              | 67.20
# Ours | 95.04559270516715  | 108.90577507598784 | 172.35396244902168  | 67.04600548035003

# Conversion factors used used to adapt our white point to get our `Ka` and `Kb`
CKA_FACTOR = CKA / (CXN + CYN)
CKB_FACTOR = CKB / (CZN + CYN)


def xyz_to_hlab(xyz: Vector, white: VectorLike) -> Vector:
    """Convert XYZ to Hunter Lab."""

    xn, yn, zn = alg.multiply(util.xy_to_xyz(white), 100, dims=alg.D1_SC)
    ka = CKA_FACTOR * (xn + yn)
    kb = CKB_FACTOR * (yn + zn)
    x, y, z = alg.multiply(xyz, 100, dims=alg.D1_SC)
    l = alg.nth_root(y / yn, 2)
    a = b = 0.0
    if l != 0:
        a = ka * (x / xn - y / yn) / l
        b = kb * (y / yn - z / zn) / l
    return [l * 100, a, b]


def hlab_to_xyz(hlab: Vector, white: VectorLike) -> Vector:
    """Convert Hunter Lab to XYZ."""

    xn, yn, zn = alg.multiply(util.xy_to_xyz(white), 100, dims=alg.D1_SC)
    ka = CKA_FACTOR * (xn + yn)
    kb = CKB_FACTOR * (yn + zn)
    l, a, b = hlab
    l /= 100
    y = (l ** 2) * yn
    x = (((a * l) / ka) + (y / yn)) * xn
    z = (((b * l) / kb) - (y / yn)) * -zn
    return alg.divide([x, y, z], 100, dims=alg.D1_SC)


class HunterLab(Lab):
    """Hunter Lab class."""

    BASE = 'xyz-d65'
    NAME = "hunter-lab"
    SERIALIZE = ("--hunter-lab",)
    WHITE = WHITES['2deg']['D65']

    @classmethod
    def to_base(cls, coords: Vector) -> Vector:
        """To XYZ from Hunter Lab."""

        return hlab_to_xyz(coords, cls.white())

    @classmethod
    def from_base(cls, coords: Vector) -> Vector:
        """From XYZ to Hunter Lab."""

        return xyz_to_hlab(coords, cls.white())

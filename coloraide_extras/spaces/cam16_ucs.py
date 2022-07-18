"""CAM16 class."""
import math
import bisect
from coloraide.spaces import Space, Labish
from coloraide.cat import WHITES
from coloraide.channels import Channel
from coloraide import util
from coloraide import algebra as alg
from coloraide.types import Vector, VectorLike
from typing import Optional, cast

M16 = [
    [0.401288, 0.650173, -0.051461],
    [-0.250268, 1.204414, 0.045854],
    [-0.002079, 0.048952, 0.953127]
]

MI6_INV = alg.inv(M16)

M1 = [
    [460.0, 451.0, 288.0],
    [460.0, -891.0, -261.0],
    [460.0, -220.0, -6300.0]
]

ADAPTED_COEF = 0.42
ADAPTED_COEF_INV = 1 / ADAPTED_COEF

SURROUND = {
    'dark': (0.8, 0.525, 0.8),
    'dim': (0.9, 0.59, 0.9),
    'average': (1, 0.69, 1)
}

COEFFICENTS = {
    'lcd': (0.77, 0.007, 0.0053),
    'scd': (1.24, 0.007, 0.0363),
    'ucs': (1.00, 0.007, 0.0228)
}

HUE_QUADRATURE = {
    # Red, Yellow, Green, Blue, Red
    "h": (20.14, 90.00, 164.25, 237.53, 380.14),
    "e": (0.8, 0.7, 1.0, 1.2, 0.8),
    "H": (0.0, 100.0, 200.0, 300.0, 400.0)
}


def hue_quadrature(h: float) -> float:
    """
    Hue to hue quadrature.

    https://onlinelibrary.wiley.com/doi/pdf/10.1002/col.22324
    """

    hp = h % 360
    if hp <= HUE_QUADRATURE['h'][0]:
        hp += 360

    i = bisect.bisect_left(HUE_QUADRATURE['h'], hp) - 1
    hi, hii = HUE_QUADRATURE['h'][i:i + 2]
    ei, eii = HUE_QUADRATURE['e'][i:i + 2]
    Hi = HUE_QUADRATURE['H'][i]

    t = (hp - hi) / ei
    return Hi + (100 * t) / (t + (hii - hp) / eii)


def inv_hue_quadrature(H: float) -> float:
    """Hue quadrature to hue."""

    Hp = H % 400
    i = math.floor(0.01 * Hp)
    Hp = Hp % 100
    hi, hii = HUE_QUADRATURE['h'][i:i + 2]
    ei, eii = HUE_QUADRATURE['e'][i:i + 2]

    return ((Hp * (eii * hi - ei * hii) - 100 * hi * eii) / (Hp * (eii - ei) - 100 * eii)) % 360


def adapt(coords: Vector, fl: float) -> Vector:
    """Adapt the coordinates."""

    adapted = []
    for c in coords:
        x = math.pow(fl * abs(c) * 0.01, ADAPTED_COEF)
        adapted.append(math.copysign(400 * x / (x + 27.13), c))
    return adapted


def unadapt(adapted: Vector, fl: float) -> Vector:
    """Remove adaptation from coordinates."""

    coords = []
    constant = 100 / fl * math.pow(27.13, ADAPTED_COEF_INV)
    for c in adapted:
        cabs = abs(c)
        coords.append(math.copysign(constant * math.pow(cabs / (400 - cabs), ADAPTED_COEF_INV), c))
    return coords


class Environment:
    """Class to calculate and contain any required environmental data (viewing conditions included)."""

    def __init__(
        self,
        coefficents: str,
        ref_white: VectorLike,
        adapting_luminance: float,
        background_luminance: float,
        surround: str,
        discounting: bool
    ):
        """
        Initialize environmental viewing conditions.

        Using the specified viewing conditions, and general environmental data,
        initialize anything that we can ahead of time to speed up the process.
        """

        xyz_w = alg.multiply(util.xy_to_xyz(ref_white), 100, dims=alg.D1_SC)

        # The average luminance of the environment in `cd/m^2cd/m` (a.k.a. nits)
        la = adapting_luminance
        # The relative luminance of the nearby background
        yb = background_luminance
        # Absolute luminance of the reference white.
        yw = xyz_w[1]

        # Cone response for reference white
        rgb_w = alg.dot(M16, xyz_w)

        # Surround: dark, dim, and average
        f, self.c, self.nc = SURROUND[surround]

        self.kl, self.c1, self.c2 = COEFFICENTS[coefficents]

        k = 1 / (5 * la + 1)
        k4 = k ** 4

        # Factor of luminance level adaptation
        self.fl = (k4 * la + 0.1 * (1 - k4) * (1 - k4) * math.pow(5 * la, 1 / 3))
        self.fl_root = math.pow(self.fl, 0.25)

        self.n = yb / yw
        self.z = 1.48 + math.sqrt(self.n)
        self.nbb = 0.725 * math.pow(self.n, -0.2)
        self.ncb = self.nbb

        # Degree of adaptation calculating if discounting illuminant (assumed eye is fully adapted)
        d = alg.clamp(f * (1 - 1 / 3.6 * math.exp((-la - 42) / 92)), 0, 1) if not discounting else 1
        self.d_rgb = [alg.lerp(1, yw / coord, d) for coord in rgb_w]
        self.d_rgb_inv = [1 / coord for coord in self.d_rgb]

        # Achromatic response
        rgb_cw = alg.multiply(rgb_w, self.d_rgb, dims=alg.D1)
        rgb_aw = adapt(rgb_cw, self.fl)
        self.a_w = self.nbb * (2 * rgb_aw[0] + rgb_aw[1] + 0.05 * rgb_aw[2])


def cam16_to_xyz_d65(
    J: Optional[float] = None,
    C: Optional[float] = None,
    h: Optional[float] = None,
    s: Optional[float] = None,
    Q: Optional[float] = None,
    M: Optional[float] = None,
    H: Optional[float] = None,
    env: Optional[Environment] = None
) -> Vector:
    """From CAM16 to XYZ."""

    # Reverse calculation can actually be obtained from a small subset of the components
    # Really, only one should be given as we won't know which one is correct otherwise,
    # but we don't currently enforce it as we expect the `Space` object to do that.
    if not ((J is not None) ^ (Q is not None)):
        raise ValueError("Conversion requires one and only one: 'J' or 'Q'")

    if not ((C is not None) ^ (M is not None) ^ (s is not None)):
        raise ValueError("Conversion requires one and only one: 'C', 'M' or 's'")

    # Hue is absolutely required
    if not ((h is not None) ^ (H is not None)):
        raise ValueError("Conversion requires one and only one: 'h' or 'H'")

    # We need viewing conditions
    if env is None:
        raise ValueError("No viewing conditions/environment provided")

    # Black
    if J == 0 or Q == 0:
        return [0, 0, 0]

    # Break hue into Cartesian components
    h_rad = math.radians(h if h is not None else inv_hue_quadrature(cast(float, H)))
    cos_h = math.cos(h_rad)
    sin_h = math.sin(h_rad)

    # Calculate `J_root` from one of the lightness derived coordinates.
    if J is not None:
        J_root = alg.nth_root(J, 2) * 0.1
    else:
        J_root = 0.25 * env.c * cast(float, Q) / ((env.a_w + 4) * env.fl_root)

    # Calculate the `t` value from one of the chroma derived coordinates
    if C is not None:
        alpha = C / J_root
    elif M is not None:
        alpha = (M / env.fl_root) / J_root
    else:
        alpha = 0.0004 * (cast(float, s) ** 2) * (env.a_w + 4) / env.c
    t = alg.npow(alpha * math.pow(1.64 - math.pow(0.29, env.n), -0.73), 10 / 9)

    # Eccentricity
    et = 0.25 * (math.cos(h_rad + 2) + 3.8)

    # Achromatic response
    A = env.a_w * alg.npow(J_root, 2 / env.c / env.z)

    # Calculate red-green and yellow-blue components
    p1 = 5e4 / 13 * env.nc * env.ncb * et
    p2 = A / env.nbb
    r = 23 * (p2 + 0.305) * t / (23 * p1 + t * (11 * cos_h + 108 * sin_h))
    a = r * cos_h
    b = r * sin_h

    # Calculate back from cone response to XYZ
    rgb_c = unadapt(alg.multiply(alg.dot(M1, [p2, a, b], dims=alg.D2_D1), 1 / 1403, dims=alg.D1_SC), env.fl)
    return alg.divide(
        alg.dot(MI6_INV, alg.multiply(rgb_c, env.d_rgb_inv, dims=alg.D1), dims=alg.D2_D1),
        100,
        dims=alg.D1_SC
    )


def xyz_d65_to_cam16(xyzd65: Vector, env: Environment) -> Vector:
    """From XYZ to CAM16."""

    # Cone response
    rgb_a = adapt(
        alg.multiply(
            alg.dot(M16, alg.multiply(xyzd65, 100, dims=alg.D1_SC), dims=alg.D2_D1),
            env.d_rgb,
            dims=alg.D1
        ),
        env.fl
    )

    # Red-green and yellow-blue components
    a = rgb_a[0] + (-12 * rgb_a[1] + rgb_a[2]) / 11
    b = (rgb_a[0] + rgb_a[1] - 2 * rgb_a[2]) / 9
    h_rad = math.atan2(b, a)

    # Eccentricity
    et = 0.25 * (math.cos(h_rad + 2) + 3.8)

    t = (
        5e4 / 13 * env.nc * env.ncb * et * math.sqrt(a ** 2 + b ** 2) /
        (rgb_a[0] + rgb_a[1] + 1.05 * rgb_a[2] + 0.305)
    )
    alpha = alg.npow(t, 0.9) * math.pow(1.64 - math.pow(0.29, env.n), 0.73)

    # Achromatic response
    A = env.nbb * (2 * rgb_a[0] + rgb_a[1] + 0.05 * rgb_a[2])

    J_root = alg.npow(A / env.a_w, 0.5 * env.c * env.z)

    # Lightness
    J = 100 * J_root ** 2

    # Brightness
    Q = (4 / env.c * J_root * (env.a_w + 4) * env.fl_root)

    # Chroma
    C = alpha * J_root

    # Colorfulness
    M = C * env.fl_root

    # Hue
    h = util.constrain_hue(math.degrees(h_rad))

    # Hue quadrature
    H = hue_quadrature(h)

    # Saturation
    s = 50 * alg.nth_root(env.c * alpha / (env.a_w + 4), 2)

    return [J, C, h, s, Q, M, H]


def xyz_d65_to_cam16_ucs(xyzd65: Vector, env: Environment) -> Vector:
    """XYZ to CAM16 UCS."""

    cam16 = xyz_d65_to_cam16(xyzd65, env)
    J, M, h = cam16[0], cam16[5], cam16[2]

    h = math.radians(h)
    M = math.log(1 + env.c2 * M) / env.c2
    a = M * math.cos(h)
    b = M * math.sin(h)

    return [
        (1 + 100 * env.c1) * J / (1 + env.c1 * J),
        a,
        b
    ]


def cam16_ucs_to_xyz_d65(ucs: Vector, env: Environment) -> Vector:
    """XYZ to CAM16 UCS."""

    J, a, b = ucs
    M = math.sqrt(a ** 2 + b ** 2)
    h = math.degrees(math.atan2(b, a))

    M = (math.exp(M * env.c2) - 1) / env.c2
    J = J / (1 - env.c1 * (J - 100))

    return cam16_to_xyz_d65(J=J, M=M, h=h, env=env)


class CAM16UCS(Labish, Space):
    """CAM16 UCS class."""

    BASE = "xyz-d65"
    NAME = "cam16-ucs"
    SERIALIZE = ("--cam16-ucs",)
    CHANNELS = (
        Channel("j", 0.0, 100.0),
        Channel("a", -100.0, 100.0),
        Channel("b", -100.0, 100.0)
    )
    CHANNEL_ALIASES = {
        "lightness": "j"
    }
    WHITE = WHITES['2deg']['D65']
    ENV = Environment('ucs', WHITE, 64 / math.pi * 0.2, 20, 'average', False)

    @classmethod
    def to_base(cls, coords: Vector) -> Vector:
        """To XYZ from CAM16."""

        return cam16_ucs_to_xyz_d65(coords, env=cls.ENV)

    @classmethod
    def from_base(cls, coords: Vector) -> Vector:
        """From XYZ to CAM16."""

        return xyz_d65_to_cam16_ucs(coords, env=cls.ENV)


class CAM16LCD(CAM16UCS):
    """CAM16 LCD class."""

    NAME = "cam16-lcd"
    SERIALIZE = ("--cam16-lcd",)
    ENV = Environment('lcd', CAM16UCS.WHITE, 64 / math.pi * 0.2, 20, 'average', False)


class CAM16SCD(CAM16UCS):
    """CAM16 SCD class."""

    NAME = "cam16-scd"
    SERIALIZE = ("--cam16-scd",)
    ENV = Environment('scd', CAM16UCS.WHITE, 64 / math.pi * 0.2, 20, 'average', False)

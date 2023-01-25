"""Calculate range in sRGB."""
import sys
import argparse
import os
import numpy as np
import math
import matplotlib.pyplot as plt

sys.path.insert(0, os.getcwd())

from coloraide_extras.everything import ColorAll as Color  # noqa: E402
from coloraide_extras.spaces.hct import HCT, y_to_lstar, POLY_COEF, LOG_COEF1, LOG_COEF2  # noqa: E402
from coloraide_extras.spaces.cam16_ucs import xyz_d65_to_cam16  # noqa: E402

CHECK_THRESH = False


def detect_achromatic(c: float, t: float) -> bool:
    """Test the current calculated coefficients in the library."""

    if t <= 0:
        c2 = 0
    elif t >= 8:
        c2 = POLY_COEF[0] * t ** 3 + POLY_COEF[1] * t ** 2 + POLY_COEF[2] * t + POLY_COEF[3]
    elif t >= 2:
        c2 = max(0, LOG_COEF1[0] * math.log(t) + LOG_COEF1[1])
    else:
        c2 = max(0, LOG_COEF2[0] * math.log(t) + LOG_COEF2[1])

    return c2


def main():
    """Main."""

    parser = argparse.ArgumentParser(
        prog='calc_hct_min_chroma.py', description='Calculate minimum chroma for achromatic colors in HCT.'
    )
    # Flag arguments
    parser.add_argument(
        '--rgb', '-r', action='store', default='srgb', help="The RGB space which the color will be sized against."
    )
    parser.add_argument(
        '--res', '-s', type=int, default=100000, help="Resolution to use when calculating range, default is 100."
    )
    args = parser.parse_args()

    return run(args.rgb, args.res)


def run(rgb, res):
    """Run."""

    color = Color('hct', [0, 0, 0])
    m = {}
    diff = 0

    for i in range(res):
        color.update('srgb', [i / res, i / res, i / res])
        xyz = color.convert('xyz-d65')
        c = xyz_d65_to_cam16(xyz[:-1], HCT.ENV)[1]
        t = y_to_lstar(xyz[1], HCT.ENV.ref_white)

        if CHECK_THRESH:
            calc = detect_achromatic(c, t)
            delta = abs(calc - c)
            if delta > diff:
                diff = delta

        if t not in m:
            m[t] = c
        elif m[t] < c:
            m[t] = c

    if CHECK_THRESH:
        print('=== Threshold ===')
        print(diff)

    # Upper T segment - linear-ish
    tu = []
    cu = []

    # Mid T segment - log-ish
    tm = []
    cm = []

    # Big T segment - log-ish
    tl = []
    cl = []

    # Gather up the tone and chroma into separate lists
    # as we will fit each section differently
    limit_lower = 2
    limit_upper = 8
    for t in sorted(m):
        if t == 0:
            continue
        elif t < limit_lower:
            tl.append(t)
            cl.append(m[t])
        elif limit_lower <= t < limit_upper:
            tm.append(t)
            cm.append(m[t])
        else:
            tu.append(t)
            cu.append(m[t])

    # Final tone and chroma combining both segments
    tf = tl[:] + tm[:] + tu[:]
    cf = cl[:] + cm[:] + cu[:]

    # Fit the small and large curves
    curve_u = list(np.polyfit(tu, cu, 3))
    curve_m = list(np.polyfit(np.log(tm), cm, 1))
    curve_l = list(np.polyfit(np.log(tl), cl, 1))

    # Chroma calculated from the tone
    cc = []
    # Print the calculated coefficients
    print('=== Upper curve coefficients ===')
    print(curve_u)
    print('=== Middle curve coefficients ===')
    print(curve_m)
    print('=== Lower curve coefficients ===')
    print(curve_l)
    for i in tf:
        if i >= limit_upper:
            cc.append(curve_u[0] * i ** 3 + curve_u[1] * i ** 2 + curve_u[2] * i + curve_u[3])
        elif i >= limit_lower:
            cc.append(curve_m[0] * math.log(i) + curve_m[1])
        else:
            cc.append(curve_l[0] * math.log(i) + curve_l[1])

    # Print the calculated line against the real line
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.plot(cf, tf, '.', color='black')
    plt.plot(cc, tf, '.', color='red')
    plt.show()

    return 0


if __name__ == "__main__":
    sys.exit(main())

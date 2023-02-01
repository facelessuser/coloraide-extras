"""
Map our achromatic spline calculation against real achromatic response.

Report the delta between our spline and the real world. Also note the highest chroma climbs.
"""
import sys
import argparse
import os
import matplotlib.pyplot as plt
import math

sys.path.insert(0, os.getcwd())

from coloraide_extras.everything import ColorAll as Color  # noqa: E402
from coloraide_extras.spaces.cam16_ucs_jmh import Environment, xyz_d65_to_cam16_ucs_jmh, Achromatic  # noqa: E402
from coloraide.cat import WHITES  # noqa: E402


def main():
    """Main."""

    parser = argparse.ArgumentParser(
        prog='calc_cam16_ucs_jmh_min_m.py',
        description='Calculate min M for achromatic colors in CAM16 UCS JMh and map current spline against real values.'
    )
    # Flag arguments
    parser.add_argument(
        '--res', '-r', type=int, default=50000, help="Resolution to use when calculating range, default is 50000."
    )
    parser.add_argument(
        '--coeff', '-c', type=str, default='ucs', help="Coefficients to use: 'ucs', 'scd', or 'lcd'."
    )
    parser.add_argument(
        '--white-point', '-w', type=str, default='2deg:D65', help="White point 'deg:wp', example: '2deg:D65'."
    )
    parser.add_argument(
        '--adapting-luminance', '-a', type=float, default=64 / math.pi * 0.2, help="Adapting luminance."
    )
    parser.add_argument(
        '--background-luminance', '-b', type=float, default=20, help="Background luminace - default 20 (gray world)."
    )
    parser.add_argument(
        '--surround', '-s', type=str, default='average', help="Surround: 'average', 'dim', 'dark'"
    )
    parser.add_argument(
        '--discounting', '-d', action='store_true', help="Enable discounting."
    )
    parser.add_argument(
        '--spline', '-S', type=str, default='catrom', help="Spline to use for approximation of achromatic line"
    )
    parser.add_argument(
        '--low', '-L', type=str, default='0:25:1:100.0',
        help="Tuning for low range: start:end:step:scale (int:int:int:float)"
    )
    parser.add_argument(
        '--mid', '-M', type=str, default='25:101:25:55.0',
        help="Tuning for mid range: start:end:step:scale (int:int:int:float)"
    )
    parser.add_argument(
        '--high', '-H', type=str, default='101:252:25:45.0',
        help="Tuning for high range: start:end:step:scale (int:int:int:float)"
    )
    args = parser.parse_args()

    return run(
        args.coeff,
        args.white_point,
        args.adapting_luminance,
        args.background_luminance,
        args.surround,
        args.discounting,
        args.spline,
        args.low,
        args.mid,
        args.high,
        args.res
    )


def run(coeff, white_point, la, ba, surround, discounting, spline, low, mid, high, res):
    """Run."""

    deg, wp = white_point.split(':')
    tuning = {
        "low": [int(i) if e < 3 else float(i) for e, i in enumerate(low.split(':'))],
        "mid": [int(i) if e < 3 else float(i) for e, i in enumerate(mid.split(':'))],
        "high": [int(i) if e < 3 else float(i) for e, i in enumerate(high.split(':'))]
    }
    env = Environment(coeff, WHITES[deg][wp], la, ba, surround, discounting)
    test = Achromatic(tuning, 0.06, env, spline)

    color = Color('srgb', [0, 0, 0])
    points1 = {}
    points2 = {}
    diff = 0
    max_m = 0
    hues = []

    for i in range(res + 1):
        div = res / 5
        color.update('srgb', [i / div, i / div, i / div])
        xyz = color.convert('xyz-d65')
        l, m, h = xyz_d65_to_cam16_ucs_jmh(xyz[:-1], env)[:]

        hues.append(h)

        if m > max_m:
            max_m = m

        domain = test.scale(l)
        calc = test.spline(domain)

        delta = abs(calc[1] - m)
        if delta > diff:
            diff = delta

        points1[l] = m
        points2[calc[0]] = calc[1]

    print('Delta: ', diff)
    print('Max M: ', max_m)
    print('Avg Achromatic Hue: ', sum(hues) / len(hues))

    l1 = []
    l2 = []
    m1 = []
    m2 = []
    for l in sorted(points1):
        l1.append(l)
        m1.append(points1[l])
    for l in sorted(points2):
        l2.append(l)
        m2.append(points2[l])

    figure = plt.figure()

    # Create axes
    ax = plt.axes(
        xlabel='M',
        ylabel='J'
    )
    ax.set_aspect('auto')
    ax.set_title('JMh: Delta = {} - Max M = {}'.format(diff, max_m))
    figure.add_axes(ax)

    # Print the calculated line against the real line
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.plot(m1, l1, '.', color='black')
    plt.plot(m2, l2, '.', color='red', markersize=0.5)
    plt.show()

    return 0


if __name__ == "__main__":
    sys.exit(main())

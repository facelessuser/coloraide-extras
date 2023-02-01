"""
Map our achromatic spline calculation against real achromatic response.

Report the delta between our spline and the real world. Also note the highest chroma climbs.
"""
import sys
import argparse
import os
import matplotlib.pyplot as plt

sys.path.insert(0, os.getcwd())

from coloraide_extras.everything import ColorAll as Color  # noqa: E402
from coloraide_extras.spaces.cam16_ucs_jmh import CAM16UCSJMh, xyz_d65_to_cam16_ucs_jmh, AchromaTest  # noqa: E402


def main():
    """Main."""

    parser = argparse.ArgumentParser(
        prog='calc_cam16_ucs_jmh_min_m.py',
        description='Calculate min M for achromatic colors in CAM16 UCS JMh and map current spline against real values.'
    )
    # Flag arguments
    parser.add_argument(
        '--res', '-s', type=int, default=50000, help="Resolution to use when calculating range, default is 50000."
    )
    args = parser.parse_args()

    return run(args.res)


def run(res):
    """Run."""

    test = AchromaTest(CAM16UCSJMh.ENV)

    color = Color('srgb', [0, 0, 0])
    points1 = {}
    points2 = {}
    diff = 0
    max_m = 0

    for i in range(res + 1):
        div = res / 5
        color.update('srgb', [i / div, i / div, i / div])
        xyz = color.convert('xyz-d65')
        l, m = xyz_d65_to_cam16_ucs_jmh(xyz[:-1], CAM16UCSJMh.ENV)[:2]

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

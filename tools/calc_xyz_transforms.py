"""Calculate XYZ conversion matrices."""
from coloraide import algebra as alg
from coloraide import util

white_d65 = util.xy_to_xyz((0.31270, 0.32900))
white_d50 = util.xy_to_xyz((0.34570, 0.35850))
white_aces = util.xy_to_xyz((0.32168, 0.33767))


def pprint(value):
    """Print the matrix."""
    print('[', end='')
    first = True
    for v in value:
        if first:
            first = False
        else:
            print(',\n ', end='')
        print(v, end='')
    print(']')


def get_matrix(wp, space):
    """Get the matrices for the specified space."""

    if space == 'aces-ap0':
        x = [0.7347, 0.0, 0.0001]
        y = [0.2653, 1.0, -0.0770]
    elif space == 'aces-ap1':
        x = [0.713, 0.165, 0.128]
        y = [0.293, 0.830, 0.044]
    else:
        raise ValueError

    m = alg.transpose([util.xy_to_xyz(xy) for xy in zip(x, y)])
    mi = alg.inv(m)
    rgb = alg.dot(mi, wp)
    rgb2xyz = alg.multiply(m, rgb)
    xyz2rgb = alg.inv(rgb2xyz)

    return rgb2xyz, xyz2rgb


if __name__ == "__main__":
    print('===== ACES =====')
    to_xyz, from_xyz = get_matrix(white_aces, 'aces-ap0')
    print('--- rgb -> xyz ---')
    pprint(to_xyz)
    print('--- xyz -> rgb ---')
    pprint(from_xyz)
    print('===== ACEScc =====')
    to_xyz, from_xyz = get_matrix(white_aces, 'aces-ap1')
    print('--- rgb -> xyz ---')
    pprint(to_xyz)
    print('--- xyz -> rgb ---')
    pprint(from_xyz)

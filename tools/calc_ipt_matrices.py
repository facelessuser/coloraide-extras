"""
Calculate IPT matrices.

https://scholarworks.rit.edu/cgi/viewcontent.cgi?article=3862&context=theses
"""
import numpy as np

np.set_printoptions(precision=None, sign='-', floatmode='unique')


def xy_to_xyz(x, y):
    """Convert `xyY` to `xyz`."""

    return [x / y, 1, (1 - x - y) / y]


white_d65 = np.asfarray(xy_to_xyz(0.31270, 0.32900))


def white_space_fixup(m):
    """
    Fix up the IPT white space.

    The IPT paper noted that the D65 white point that they use was [0.9504, 1.0, 1.0889].
    This is not the white point we use, so actual precision of the color space breaks down
    and doesn't match implementations that do use the above white point.

    If we look at Colour Science, we can see that when using the above white point, that
    precision around white is much better:

    ```
    >>> import colour
    >>> import numpy as np
    >>> XYZ = np.array([0.9504, 1.0, 1.0889])
    >>> colour.XYZ_to_IPT(XYZ).tolist()
    [0.9999910919149724, 6.691134620062655e-05, -3.9005477081299755e-05]
    ```

    But what we got was:

    ```
    >>> from coloraide import Color
    >>> from coloraide_extras.spaces.ipt import IPT
    >>> class ColorX(Color): ...
    ...
    >>> ColorX.register(IPT)
    >>> ColorX('white').convert('ipt').coords()
    [1.0000046779854483, 0.00011652905964981697, -0.00010857262923669175]
    ```

    Clearly, this is because of a different white point. By simply removing the
    previous white point and adding ours in, we get comparable results.

    ```
    >>> from coloraide import Color
    >>> from coloraide_extras.spaces.ipt import IPT
    >>> class ColorX(Color): ...
    ...
    >>> ColorX.register(IPT)
    >>> ColorX('white').convert('ipt').coords()
    [0.9999910919149725, 6.69113462008486e-05, -3.900547708157731e-05]
    ```
    """

    theirs = np.diag([0.9504, 1.0, 1.0889])
    ours = np.diag(white_d65)

    return np.dot(np.dot(m, theirs), np.linalg.inv(ours))


m1 = np.asfarray(
    [
        [0.4002, 0.7075, -0.0807],
        [-0.2280, 1.1500, 0.0612],
        [0.0, 0.0, 0.9184]
    ]
)

m1 = white_space_fixup(m1)

m2 = np.asfarray(
    [
        [0.4000, 0.4000, 0.2000],
        [4.4550, -4.8510, 0.3960],
        [0.8056, 0.3572, -1.1628]
    ]
)


if __name__ == "__main__":
    print('===== XYZ to LMS =====')
    print(m1)
    print('===== LMS to XYZ =====')
    print(np.linalg.inv(m1))
    print('===== LMS to IPT =====')
    print(m2)
    print('===== IPT to LMS =====')
    print(np.linalg.inv(m2))

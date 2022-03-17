"""
Calculate IgPgTg matricies.

https://www.ingentaconnect.com/content/ist/jpi/2020/00000003/00000002/art00002#
"""
import numpy as np

np.set_printoptions(precision=None, sign='-', floatmode='unique')

m1 = np.asfarray(
    [
        [2.968, 2.741, -0.649],
        [1.237, 5.969, -0.173],
        [-0.318, 0.387, 2.311]
    ]
)

m2 = np.asfarray(
    [
        [0.117, 1.464, 0.130],
        [8.285, -8.361, 21.40],
        [-1.208, 2.412, -36.53]
    ]
)


if __name__ == "__main__":
    print('===== XYZ to LMS =====')
    print(m1)
    print('===== LMS to XYZ =====')
    print(np.linalg.inv(m1))
    print('===== LMS to IgPgTg =====')
    print(m2)
    print('===== IgPgTg to LMS =====')
    print(np.linalg.inv(m2))

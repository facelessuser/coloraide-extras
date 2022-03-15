"""
Calculate IgTgPg matricies.

https://scholarworks.rit.edu/cgi/viewcontent.cgi?article=3862&context=theses
"""
import numpy as np

np.set_printoptions(precision=None, sign='-', floatmode='unique')

m1 = np.asfarray(
    [
        [0.4002, 0.7075, -0.0807],
        [-0.2280, 1.1500, 0.0612],
        [0.0, 0.0, 0.9184]
    ]
)

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

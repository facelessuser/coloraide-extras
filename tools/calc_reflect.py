"""
Calculate reflection curves.

Approaches comes from Scott Burns.
http://scottburns.us/matlab-octave-and-python-source-code-for-refl-recon-chrom-adapt/
"""
import sys
import os
import math
import matplotlib.pyplot as plt

sys.path.insert(0, os.getcwd())

from coloraide import algebra as alg  # noqa: E402
from coloraide.everything import ColorAll as Color  # noqa: E402
from coloraide.cmfs import CIE_1931_2DEG as CMF  # noqa: E402

targets = ['#ff0000', '#00ff00', '#0000ff', '#00ffff', '#ff00ff', '#ffff00']
space = 'srgb'
START = 380
STEP = 10
END = 750 + STEP
MAX_ITERS = 50
EPSILON = 1e-15
METHOD = 3

D65 = {
    300: 0.034100,
    305: 1.664300,
    310: 3.294500,
    315: 11.765200,
    320: 20.236000,
    325: 28.644700,
    330: 37.053500,
    335: 38.501100,
    340: 39.948800,
    345: 42.430200,
    350: 44.911700,
    355: 45.775000,
    360: 46.638300,
    365: 49.363700,
    370: 52.089100,
    375: 51.032300,
    380: 49.975500,
    385: 52.311800,
    390: 54.648200,
    395: 68.701500,
    400: 82.754900,
    405: 87.120400,
    410: 91.486000,
    415: 92.458900,
    420: 93.431800,
    425: 90.057000,
    430: 86.682300,
    435: 95.773600,
    440: 104.865000,
    445: 110.936000,
    450: 117.008000,
    455: 117.410000,
    460: 117.812000,
    465: 116.336000,
    470: 114.861000,
    475: 115.392000,
    480: 115.923000,
    485: 112.367000,
    490: 108.811000,
    495: 109.082000,
    500: 109.354000,
    505: 108.578000,
    510: 107.802000,
    515: 106.296000,
    520: 104.790000,
    525: 106.239000,
    530: 107.689000,
    535: 106.047000,
    540: 104.405000,
    545: 104.225000,
    550: 104.046000,
    555: 102.023000,
    560: 100.000000,
    565: 98.167100,
    570: 96.334200,
    575: 96.061100,
    580: 95.788000,
    585: 92.236800,
    590: 88.685600,
    595: 89.345900,
    600: 90.006200,
    605: 89.802600,
    610: 89.599100,
    615: 88.648900,
    620: 87.698700,
    625: 85.493600,
    630: 83.288600,
    635: 83.493900,
    640: 83.699200,
    645: 81.863000,
    650: 80.026800,
    655: 80.120700,
    660: 80.214600,
    665: 81.246200,
    670: 82.277800,
    675: 80.281000,
    680: 78.284200,
    685: 74.002700,
    690: 69.721300,
    695: 70.665200,
    700: 71.609100,
    705: 72.979000,
    710: 74.349000,
    715: 67.976500,
    720: 61.604000,
    725: 65.744800,
    730: 69.885600,
    735: 72.486300,
    740: 75.087000,
    745: 69.339800,
    750: 63.592700,
    755: 55.005400,
    760: 46.418200,
    765: 56.611800,
    770: 66.805400,
    775: 65.094100,
    780: 63.382800
}

if space == 'srgb':
    from coloraide.spaces.srgb_linear import XYZ_TO_RGB
elif space == 'display-p3':
    from coloraide.spaces.display_p3_linear import XYZ_TO_RGB
elif space == 'a98-rgb':
    from coloraide.spaces.a98_rgb_linear import XYZ_TO_RGB
elif space == 'rec2020':
    XYZ_TO_RGB = [
        [1.7249510969855462, -0.36225403975096726, -0.2545649705534804],
        [-0.6692669194491035, 1.6225096012804534, 0.012487041279557484],
        [0.018196517838035248, -0.04443708810957042, 0.9431475044937067]
    ]
else:
    raise ValueError('Cannot perfrom operation on this space')


A = [[], [], []]
for r in range(START, END, STEP):
    A[0].append(CMF[r][0])
    A[1].append(CMF[r][1])
    A[2].append(CMF[r][2])

W = [D65[r] for r in range(START, END, STEP)]

value = alg.matmul(A, alg.diag(W))
w = alg.vdot(A[1], W)

# Illuminant referenced CMFs
T = alg.divide(value, w)

# Make in relation to the RGB color space
TRGB = alg.matmul(XYZ_TO_RGB, T)

# Array of finite differencing constants
size = len(W)
fill = {-1: -2, 0: 4, 1: -2}
D = [[fill.get(i - j, 0) for j in range(size)] for i in range(size)]
D[0][0] = 2
D[size - 1][size - 1] = 2

# Vectorize some functions we will use
exp = alg.vectorize2(math.exp, params=1)
tanh = alg.vectorize2(math.tanh, params=1)


def _exp(x):
    """This can overflow, so clamp the result to zero."""
    try:
        return math.exp(x)
    except OverflowError:
        return 0


def _sech2(x):
    """This can overflow, so clamp the result to zero."""
    try:
        return 1 / (math.cosh(x) ** 2)
    except OverflowError:
        return 0

sech2 = alg.vectorize2(_sech2, params=1)
exp = alg.vectorize2(_exp, params=1)


def method_2(d, cmfs_w, XYZ_w, max_iterations=MAX_ITERS, tolerance=EPSILON):
    """
    Estimate reflectance curve.

    Computes a reconstructed spectral reflectance curve from
    an illuminant-referenced triplet of tristimulus values
    representing a real color (within the spectral locus).

    Parameters
    ----------
    `d`: nxn array of finite differencing constants, obtained
           from function `method_2_prep.py`. (n is the number
           of wavelength bins (rows) used in the CMFs.)
    `cmfs_w`: nx3 array of illuminant-w-referenced CMFs,
           obtained from function `method_2_prep.py`.
    `XYZ_w`: a three element vector of illum-w-referenced
           tristimulus values in the 0 <= Y <= 1 convention range.
    max_iterations: upper limit on iterations (defaults to 20).
    tolerance: determines when the linear equations for a
           stationary point are satisfied (default is 1e-8).

    Returns
    -------
    nx1 vector of spectral reflectance values (or zeros if failure).

    Notes
    -----
    The input parameters d and `cmfs_w` can be generated by function
    `method_2_prep.py`. For a given illuminant, `method_2_prep`
    needs to be called only once. Multiple calls to `method_2`
    may then follow for various tristimulus values. This is a
    typical use case, and avoids repeated computation of d and
    `cmfs_w`.

    The XYZ_w supplied to `method_2` must fall strictly within the
    spectral locus (i.e., be a real color), or the method will fail
    and return a vector of zeros.

    The reflectance curve generated will always have positive
    values, but may have some values >1 (which can be interpreted
    as an emissive source divided by the illuminant). To obtain
    reflectance curves strictly in the range 0 to 1, representing
    valid object reflectances, use `method_3.py` instead.

    `method_2` is based on "method 2" of Reference [1]. It also
    corresponds to method "LLSS" (Least Log Slope Squared) of
    Reference [2].

    References
    ----------
    [1] Burns SA. Numerical methods for smoothest reflectance
        reconstruction. Color Research & Application, Vol 45,
        No 1, 2020, pp 8-21.
    [2] Generating Reflectance Curves from sRGB Triplets, 2015
        http://scottburns.us/reflectance-curves-from-srgb/#LLSS

    Acknowledgements
    ----------------
    Thanks to Adam J. Burns and Mark (`kram1032`) for assistance
    with translating from MATLAB to Python.
    """

    n = len(cmfs_w)
    z = alg.zeros(n)
    lamb = alg.zeros(3)
    for _ in range(max_iterations):
        r = exp(z)
        dr = alg.diag(r)
        dra = alg.matmul(dr, cmfs_w)
        v = alg.matmul(dra, lamb)
        p1 = alg.add(alg.matmul(d, z), v)
        p2 = alg.subtract(alg.matmul(alg.transpose(cmfs_w), r), XYZ_w)
        F = p1 + p2
        p1 = alg.add(d, alg.diag(v))
        p2 = dra
        p3 = alg.transpose(dra)
        p4 = alg.zeros((3, 3))
        for x1, y1 in zip(p1, p2):
            x1.extend(y1)
        for x1, y1 in zip(p3, p4):
            x1.extend(y1)
        p1.extend(p3)
        J = p1
        try:
            try:
                delta = alg.solve(J, alg.multiply(F, -1))
            except Exception:
                pi = alg.pinv(J)
                delta = alg.dot(pi, alg.multiply(F, -1))
        except Exception:
            print('Ill-conditioned or singular linear system detected.')
            print(f'Check to make sure XYZ_w {XYZ_w} is within the spectral locus.')
            return alg.zeros(n)
        z = alg.add(z, delta[:n])
        lamb = alg.add(lamb, delta[n:])
        if alg.all([abs(f) < tolerance for f in F]):
            return exp(z)
    print('Maximum number of iterations reached.')
    print('Check to make sure XYZ_w is within the spectral locus.')
    return alg.zeros(n)


def method_3(d, cmfs_w, XYZ_w, max_iterations=MAX_ITERS, tolerance=EPSILON):
    """
    Estimate reflectance curve.

    Computes a reconstructed spectral reflectance curve from
    an illuminant-referenced triplet of tristimulus values
    representing an object color (within the object color solid).

    Parameters
    ----------
    `d`: nxn array of finite differencing constants, obtained
           from function `method_3_prep.py`. (n is the number
           of wavelength bins (rows) used in the CMFs.)
    `cmfs_w`: nx3 array of illuminant-w-referenced CMFs,
           obtained from function `method_3_prep.py`.
    `XYZ_w`: a three element vector of illum-w-referenced
           tristimulus values in the 0 <= Y <= 1 convention range.
    max_iterations: upper limit on iterations (defaults to 20).
    tolerance: determines when the linear equations for a
           stationary point are satisfied (default is 1e-8).

    Returns
    -------
    nx1 vector of spectral reflectance values (or zeros if failure).

    Notes
    -----
    The input parameters d and `cmfs_w` can be generated by function
    `method_3_prep.py`. For a given illuminant, `method_3_prep`
    needs to be called only once. Multiple calls to `method_3`
    may then follow for various tristimulus values. This is a
    typical use case, and avoids repeated computation of d and
    `cmfs_w`.

    The XYZ_w supplied to `method_3` must fall strictly within the
    object color solid (i.e., be a valid object color that can be
    represented by a reflectance curve strictly between 0 and 1),
    or the method will fail and return a vector of zeros.

    The reflectance curve generated will always have values in
    the range 0 to 1, corresponding to valid object colors. If
    it is desired to expand the applicability of the method to
    any real color within the spectral locus (including emissive
    colors), use `method_2.py` instead.

    `method_3` is based on "method 3" of Reference [1]. It also
    corresponds to method "LHTSS" (Least Hyperbolic Tangent Slope
    Squared) of Reference [2].

    References
    ----------
    [1] Burns SA. Numerical methods for smoothest reflectance
        reconstruction. Color Research & Application, Vol 45,
        No 1, 2020, pp 8-21.
    [2] Generating Reflectance Curves from sRGB Triplets, 2015
        http://scottburns.us/reflectance-curves-from-srgb/#LHTSS

    Acknowledgements
    ----------------
    Thanks to Adam J. Burns and Mark (`kram1032`) for assistance
    with translating from MATLAB to Python.

    """

    n = len(cmfs_w)  # number of rows
    z = alg.zeros(n)
    lam = alg.zeros(3)
    for _ in range(max_iterations):
        r = alg.divide(alg.add(tanh(z), 1), 2)
        s2 = sech2(z)
        d1 = alg.diag(alg.divide(s2, 2))
        d1a = alg.dot(d1, cmfs_w)
        d2 = alg.diag(alg.multiply(s2, tanh(z)))

        p1 = alg.add(alg.dot(d, z), alg.dot(d1a, lam))
        p2 = alg.subtract(alg.dot(alg.transpose(cmfs_w), r), XYZ_w)
        f = p1 + p2

        p1 = alg.subtract(d, alg.diag(alg.dot(alg.dot(d2, cmfs_w), lam)))
        p2 = d1a
        p3 = alg.transpose(d1a)
        p4 = alg.zeros((3, 3))
        for x1, y1 in zip(p1, p2):
            x1.extend(y1)
        for x1, y1 in zip(p3, p4):
            x1.extend(y1)
        p1.extend(p3)
        j = p1

        try:
            try:
                delta = alg.solve(j, alg.multiply(-1, f))
            except Exception:
                pi = alg.pinv(j)
                delta = alg.dot(pi, alg.multiply(f, -1))
        except Exception:
            print('Ill-conditioned or singular linear system detected.')
            print(f'Check to make sure XYZ_w {XYZ_w} is within the spectral locus.')
            return alg.zeros(n)
        z = alg.add(z, delta[0:n])
        lam = alg.add(lam, delta[n:n+3])
        if alg.all([abs(_f) < tolerance for _f in f]):
            return alg.divide(alg.add(tanh(z), 1), 2)
    print('Maximum number of iterations reached.')
    print('Check to make sure XYZ_w is within the object color solid.')
    return alg.zeros(n)

pcolors = []
rcolors = []
# Estimate curves for the specified colors red, green, and blue
rho = []
for c in ([1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 1, 1], [1, 0, 1], [1, 1, 0]):
    if METHOD == 3:
        r = method_3(D, alg.transpose(TRGB), c)
    elif METHOD == 2:
        r = method_2(D, alg.transpose(TRGB), c)
    else:
        raise ValueError('Unrecognized method')
    rho.append(r)

# Calculate concentration to XYZ matrix
M = alg.dot(T, list(zip(*rho)))

# Let's assume full rank. If it isn't, we'll get a singular matrix error.
# If it fails it would require a more advanced approach to try and invert.
pM = alg.pinv(M)  # noqa: N816

# Print out some conversions back and forth so we can see if we get negative results
# above and beyond floating point error.
print('=== Test Conversions ===')
for test in ('#191248', 'red', 'green', 'blue', 'cyan', 'magenta', 'yellow'):
    color = Color(test)
    ans = alg.dot(pM, color.convert('xyz-d65').coords())
    print('Uncorrected', ans)
    ans = [alg.clamp(c, 0, None) for c in ans]
    print('Corrected', ans)
    print(color.to_string(), color[:-1])
    color2 = Color('xyz-d65', alg.dot(M, ans)).convert(color.space(), in_place=True)
    print(color2.to_string(), color2[:-1])

print('=== Concentrations to XYZ ===')
alg.pprint(M)

print('=== XYZ to Concentrations ===')
alg.pprint(pM)

print('=== CMFs D65 ===')
alg.pprint(T)

# Setup plot for results
plt.style.use('seaborn-v0_8-darkgrid')
# Create axes
ax = plt.axes(
    xlabel='Wavelength',
    ylabel='Reflection'
)

for target, r in zip(targets, rho):
    print(f'==== Curve for {target} ====')
    alg.pprint(r)
    plt.plot(
        list(range(START, END, STEP)),
        r,
        color=target,
        marker="",
        linewidth=1.5,
        markersize=2,
    antialiased=True
)

plt.gcf().set_dpi(200)
plt.show()

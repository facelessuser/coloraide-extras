"""
Calculate reflection curves.

Approaches comes from Scott Burns.
http://scottburns.us/matlab-octave-and-python-source-code-for-refl-recon-chrom-adapt/
"""
import sys
import os
import math
import plotly.graph_objects as go

sys.path.insert(0, os.getcwd())

from coloraide import algebra as alg  # noqa: E402
from coloraide.everything import ColorAll as Color  # noqa: E402
from coloraide.cmfs import CIE_1931_2DEG as CMF  # noqa: E402

targets = ['#ff0000', '#00ff00', '#0000ff', '#00ffff', '#ff00ff', '#ffff00', '#ffffff']
space = 'srgb'
# With the current settings, method2 requires an epsilon of 1e-14, while method 3 can use 1e-15
# More iterations may be required for for higher step resolutions.
# For our purposes, method 3 delivers colors with estimated reflectance below 1.
# Sum of RGB is close to 1.
START = 380
STEP = 10
END = 750 + STEP
MAX_ITERS = 50
METHOD = 3
EPSILON = 1e-15 if METHOD == 3 else 1e-14

# Values at 1 nanometers
D65 = {
    300: 0.0341,
    301: 0.36014,
    302: 0.68618,
    303: 1.01222,
    304: 1.33826,
    305: 1.6643,
    306: 1.99034,
    307: 2.31638,
    308: 2.64242,
    309: 2.96846,
    310: 3.2945,
    311: 4.98865,
    312: 6.6828,
    313: 8.37695,
    314: 10.0711,
    315: 11.7652,
    316: 13.4594,
    317: 15.1535,
    318: 16.8477,
    319: 18.5418,
    320: 20.236,
    321: 21.9177,
    322: 23.5995,
    323: 25.2812,
    324: 26.963,
    325: 28.6447,
    326: 30.3265,
    327: 32.0082,
    328: 33.69,
    329: 35.3717,
    330: 37.0535,
    331: 37.343,
    332: 37.6326,
    333: 37.9221,
    334: 38.2116,
    335: 38.5011,
    336: 38.7907,
    337: 39.0802,
    338: 39.3697,
    339: 39.6593,
    340: 39.9488,
    341: 40.4451,
    342: 40.9414,
    343: 41.4377,
    344: 41.934,
    345: 42.4302,
    346: 42.9265,
    347: 43.4228,
    348: 43.9191,
    349: 44.4154,
    350: 44.9117,
    351: 45.0844,
    352: 45.257,
    353: 45.4297,
    354: 45.6023,
    355: 45.775,
    356: 45.9477,
    357: 46.1203,
    358: 46.293,
    359: 46.4656,
    360: 46.6383,
    361: 47.1834,
    362: 47.7285,
    363: 48.2735,
    364: 48.8186,
    365: 49.3637,
    366: 49.9088,
    367: 50.4539,
    368: 50.9989,
    369: 51.544,
    370: 52.0891,
    371: 51.8777,
    372: 51.6664,
    373: 51.455,
    374: 51.2437,
    375: 51.0323,
    376: 50.8209,
    377: 50.6096,
    378: 50.3982,
    379: 50.1869,
    380: 49.9755,
    381: 50.4428,
    382: 50.91,
    383: 51.3773,
    384: 51.8446,
    385: 52.3118,
    386: 52.7791,
    387: 53.2464,
    388: 53.7137,
    389: 54.1809,
    390: 54.6482,
    391: 57.4589,
    392: 60.2695,
    393: 63.0802,
    394: 65.8909,
    395: 68.7015,
    396: 71.5122,
    397: 74.3229,
    398: 77.1336,
    399: 79.9442,
    400: 82.7549,
    401: 83.628,
    402: 84.5011,
    403: 85.3742,
    404: 86.2473,
    405: 87.1204,
    406: 87.9936,
    407: 88.8667,
    408: 89.7398,
    409: 90.6129,
    410: 91.486,
    411: 91.6806,
    412: 91.8752,
    413: 92.0697,
    414: 92.2643,
    415: 92.4589,
    416: 92.6535,
    417: 92.8481,
    418: 93.0426,
    419: 93.2372,
    420: 93.4318,
    421: 92.7568,
    422: 92.0819,
    423: 91.4069,
    424: 90.732,
    425: 90.057,
    426: 89.3821,
    427: 88.7071,
    428: 88.0322,
    429: 87.3572,
    430: 86.6823,
    431: 88.5006,
    432: 90.3188,
    433: 92.1371,
    434: 93.9554,
    435: 95.7736,
    436: 97.5919,
    437: 99.4102,
    438: 101.228,
    439: 103.047,
    440: 104.865,
    441: 106.079,
    442: 107.294,
    443: 108.508,
    444: 109.722,
    445: 110.936,
    446: 112.151,
    447: 113.365,
    448: 114.579,
    449: 115.794,
    450: 117.008,
    451: 117.088,
    452: 117.169,
    453: 117.249,
    454: 117.33,
    455: 117.41,
    456: 117.49,
    457: 117.571,
    458: 117.651,
    459: 117.732,
    460: 117.812,
    461: 117.517,
    462: 117.222,
    463: 116.927,
    464: 116.632,
    465: 116.336,
    466: 116.041,
    467: 115.746,
    468: 115.451,
    469: 115.156,
    470: 114.861,
    471: 114.967,
    472: 115.073,
    473: 115.18,
    474: 115.286,
    475: 115.392,
    476: 115.498,
    477: 115.604,
    478: 115.711,
    479: 115.817,
    480: 115.923,
    481: 115.212,
    482: 114.501,
    483: 113.789,
    484: 113.078,
    485: 112.367,
    486: 111.656,
    487: 110.945,
    488: 110.233,
    489: 109.522,
    490: 108.811,
    491: 108.865,
    492: 108.92,
    493: 108.974,
    494: 109.028,
    495: 109.082,
    496: 109.137,
    497: 109.191,
    498: 109.245,
    499: 109.3,
    500: 109.354,
    501: 109.199,
    502: 109.044,
    503: 108.888,
    504: 108.733,
    505: 108.578,
    506: 108.423,
    507: 108.268,
    508: 108.112,
    509: 107.957,
    510: 107.802,
    511: 107.501,
    512: 107.2,
    513: 106.898,
    514: 106.597,
    515: 106.296,
    516: 105.995,
    517: 105.694,
    518: 105.392,
    519: 105.091,
    520: 104.79,
    521: 105.08,
    522: 105.37,
    523: 105.66,
    524: 105.95,
    525: 106.239,
    526: 106.529,
    527: 106.819,
    528: 107.109,
    529: 107.399,
    530: 107.689,
    531: 107.361,
    532: 107.032,
    533: 106.704,
    534: 106.375,
    535: 106.047,
    536: 105.719,
    537: 105.39,
    538: 105.062,
    539: 104.733,
    540: 104.405,
    541: 104.369,
    542: 104.333,
    543: 104.297,
    544: 104.261,
    545: 104.225,
    546: 104.19,
    547: 104.154,
    548: 104.118,
    549: 104.082,
    550: 104.046,
    551: 103.641,
    552: 103.237,
    553: 102.832,
    554: 102.428,
    555: 102.023,
    556: 101.618,
    557: 101.214,
    558: 100.809,
    559: 100.405,
    560: 100,
    561: 99.6334,
    562: 99.2668,
    563: 98.9003,
    564: 98.5337,
    565: 98.1671,
    566: 97.8005,
    567: 97.4339,
    568: 97.0674,
    569: 96.7008,
    570: 96.3342,
    571: 96.2796,
    572: 96.225,
    573: 96.1703,
    574: 96.1157,
    575: 96.0611,
    576: 96.0065,
    577: 95.9519,
    578: 95.8972,
    579: 95.8426,
    580: 95.788,
    581: 95.0778,
    582: 94.3675,
    583: 93.6573,
    584: 92.947,
    585: 92.2368,
    586: 91.5266,
    587: 90.8163,
    588: 90.1061,
    589: 89.3958,
    590: 88.6856,
    591: 88.8177,
    592: 88.9497,
    593: 89.0818,
    594: 89.2138,
    595: 89.3459,
    596: 89.478,
    597: 89.61,
    598: 89.7421,
    599: 89.8741,
    600: 90.0062,
    601: 89.9655,
    602: 89.9248,
    603: 89.8841,
    604: 89.8434,
    605: 89.8026,
    606: 89.7619,
    607: 89.7212,
    608: 89.6805,
    609: 89.6398,
    610: 89.5991,
    611: 89.4091,
    612: 89.219,
    613: 89.029,
    614: 88.8389,
    615: 88.6489,
    616: 88.4589,
    617: 88.2688,
    618: 88.0788,
    619: 87.8887,
    620: 87.6987,
    621: 87.2577,
    622: 86.8167,
    623: 86.3757,
    624: 85.9347,
    625: 85.4936,
    626: 85.0526,
    627: 84.6116,
    628: 84.1706,
    629: 83.7296,
    630: 83.2886,
    631: 83.3297,
    632: 83.3707,
    633: 83.4118,
    634: 83.4528,
    635: 83.4939,
    636: 83.535,
    637: 83.576,
    638: 83.6171,
    639: 83.6581,
    640: 83.6992,
    641: 83.332,
    642: 82.9647,
    643: 82.5975,
    644: 82.2302,
    645: 81.863,
    646: 81.4958,
    647: 81.1285,
    648: 80.7613,
    649: 80.394,
    650: 80.0268,
    651: 80.0456,
    652: 80.0644,
    653: 80.0831,
    654: 80.1019,
    655: 80.1207,
    656: 80.1395,
    657: 80.1583,
    658: 80.177,
    659: 80.1958,
    660: 80.2146,
    661: 80.4209,
    662: 80.6272,
    663: 80.8336,
    664: 81.0399,
    665: 81.2462,
    666: 81.4525,
    667: 81.6588,
    668: 81.8652,
    669: 82.0715,
    670: 82.2778,
    671: 81.8784,
    672: 81.4791,
    673: 81.0797,
    674: 80.6804,
    675: 80.281,
    676: 79.8816,
    677: 79.4823,
    678: 79.0829,
    679: 78.6836,
    680: 78.2842,
    681: 77.4279,
    682: 76.5716,
    683: 75.7153,
    684: 74.859,
    685: 74.0027,
    686: 73.1465,
    687: 72.2902,
    688: 71.4339,
    689: 70.5776,
    690: 69.7213,
    691: 69.9101,
    692: 70.0989,
    693: 70.2876,
    694: 70.4764,
    695: 70.6652,
    696: 70.854,
    697: 71.0428,
    698: 71.2315,
    699: 71.4203,
    700: 71.6091,
    701: 71.8831,
    702: 72.1571,
    703: 72.4311,
    704: 72.7051,
    705: 72.979,
    706: 73.253,
    707: 73.527,
    708: 73.801,
    709: 74.075,
    710: 74.349,
    711: 73.0745,
    712: 71.8,
    713: 70.5255,
    714: 69.251,
    715: 67.9765,
    716: 66.702,
    717: 65.4275,
    718: 64.153,
    719: 62.8785,
    720: 61.604,
    721: 62.4322,
    722: 63.2603,
    723: 64.0885,
    724: 64.9166,
    725: 65.7448,
    726: 66.573,
    727: 67.4011,
    728: 68.2293,
    729: 69.0574,
    730: 69.8856,
    731: 70.4057,
    732: 70.9259,
    733: 71.446,
    734: 71.9662,
    735: 72.4863,
    736: 73.0064,
    737: 73.5266,
    738: 74.0467,
    739: 74.5669,
    740: 75.087,
    741: 73.9376,
    742: 72.7881,
    743: 71.6387,
    744: 70.4893,
    745: 69.3398,
    746: 68.1904,
    747: 67.041,
    748: 65.8916,
    749: 64.7421,
    750: 63.5927,
    751: 61.8752,
    752: 60.1578,
    753: 58.4403,
    754: 56.7229,
    755: 55.0054,
    756: 53.288,
    757: 51.5705,
    758: 49.8531,
    759: 48.1356,
    760: 46.4182,
    761: 48.4569,
    762: 50.4956,
    763: 52.5344,
    764: 54.5731,
    765: 56.6118,
    766: 58.6505,
    767: 60.6892,
    768: 62.728,
    769: 64.7667,
    770: 66.8054,
    771: 66.4631,
    772: 66.1209,
    773: 65.7786,
    774: 65.4364,
    775: 65.0941,
    776: 64.7518,
    777: 64.4096,
    778: 64.0673,
    779: 63.7251,
    780: 63.3828,
    781: 63.4749,
    782: 63.567,
    783: 63.6592,
    784: 63.7513,
    785: 63.8434,
    786: 63.9355,
    787: 64.0276,
    788: 64.1198,
    789: 64.2119,
    790: 64.304,
    791: 63.8188,
    792: 63.3336,
    793: 62.8484,
    794: 62.3632,
    795: 61.8779,
    796: 61.3927,
    797: 60.9075,
    798: 60.4223,
    799: 59.9371,
    800: 59.4519,
    801: 58.7026,
    802: 57.9533,
    803: 57.204,
    804: 56.4547,
    805: 55.7054,
    806: 54.9562,
    807: 54.2069,
    808: 53.4576,
    809: 52.7083,
    810: 51.959,
    811: 52.5072,
    812: 53.0553,
    813: 53.6035,
    814: 54.1516,
    815: 54.6998,
    816: 55.248,
    817: 55.7961,
    818: 56.3443,
    819: 56.8924,
    820: 57.4406,
    821: 57.7278,
    822: 58.015,
    823: 58.3022,
    824: 58.5894,
    825: 58.8765,
    826: 59.1637,
    827: 59.4509,
    828: 59.7381,
    829: 60.0253,
    830: 60.3125
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

# Vectorize some functions we will use.
# If any of the functions overflow, return zero.
# `exp` is most likely to do this, the others may not unless pushed too hard.
def _tanh(x):
    """Clamp the results to zero if there is overflow."""

    try:
        return math.tanh(x)
    except OverflowError:
        return 0


def _exp(x):
    """Clamp the results to zero if there is overflow."""

    try:
        return math.exp(x)
    except OverflowError:
        return 0


def _sech2(x):
    """Clamp the results to zero if there is overflow."""

    try:
        return 1 / (math.cosh(x) ** 2)
    except OverflowError:
        return 0


tanh = alg.vectorize2(_tanh, params=1)
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


# Estimate curves for the specified colors red, green, blue, cyan, and magenta.
rho = []
for color in targets:
    c = Color(color).convert('srgb-linear').coords()
    METHOD = 2 if c == [1, 1, 1] else 3
    EPSILON = 1e-15 if METHOD == 3 else 1e-14
    if METHOD == 3:
        r = method_3(D, alg.transpose(TRGB), c)
    elif METHOD == 2:
        r = method_2(D, alg.transpose(TRGB), c)
    else:
        raise ValueError('Unrecognized method')
    rho.append(r)

print('=== CMFs D65 ===')
print('==== X ====')
alg.pprint(T[0])
print('==== Y ====')
alg.pprint(T[1])
print('==== Z ====')
alg.pprint(T[2])

# Setup plot for results
fig = go.Figure(
    layout={
        'title': 'Primary Color Reflectance Curves',
        'xaxis_title': 'Wavelength',
        'yaxis_title': 'Reflection',
        'width': 800,
        'height': 600
    }
)

print('=== Reflectance Curves ===')
for target, r in zip(targets, rho):
    print(f'==== Curve for {target} ====')
    alg.pprint(r)

    fig.add_traces(data=go.Scatter(
        x=list(range(START, END, STEP)),
        y=r,
        mode="lines",
        line={'color': target, 'width': 4, 'shape': 'spline'},
        showlegend=False
    ))

fig.show('browser')

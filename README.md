# ColorAide Extras

A place to house uncommon and experimental color spaces, ∆E methods, and gamut mapping methods not currently intended
for the main [ColorAide](https://github.com/facelessuser/coloraide) repository.

Some may be quite polished, and some may be a work in progress.

Requires ColorAide to already be installed:

```console
$ pip install coloraide_extras
```

You can either cherry pick plugins you want:

```py
>>> from coloraide import Color as Base
>>> from coloraide_extras.spaces.hunter_lab import HunterLab
>>> class Color(Base):
... 
>>> Color.register(HunterLab)
>>> Color('red').convert('hunter-lab')
color(--hunter-lab 46.113 82.694 28.337 / 1)
```

Or just use the provided color class that includes all the default ColorAide color spaces, plus the extras!

```py
>>> from coloraide_extras import Color
>>> Color('red').convert('hunter-lab')
color(--hunter-lab 46.113 82.694 28.337 / 1)
```

## Spaces

### CMY

```py
>>> Color('red').convert('cmy')
color(--cmy 0 1 1 / 1)
```

The CMY color model is a subtractive color model in which cyan, magenta and yellow pigments or dyes are added together
in various ways to reproduce a broad array of colors. The name of the model comes from the initials of the three
subtractive primary colors: cyan, magenta, and yellow.

[Learn more](https://en.wikipedia.org/wiki/CMY_color_model).

![CMY](https://github.com/facelessuser/coloraide-extras/blob/main/images/cmy.png)

### CMYK

```py
>>> Color('red').convert('cmyk')
color(--cmyk 0 1 1 0 / 1)
```

Similar to the [CMY](#cmy) model and is used in the printing industry. CMYK is usually a calibrated model. The ColorAide
model is a simple naive representation.

CMYK refers to the four inks used in some color printing: cyan, magenta, yellow, and key. It uses K, black ink, since
C, M, and Y inks are translucent and will only produce a gray color when laid on top of each other.

[Learn more](https://en.wikipedia.org/wiki/CMY_color_model).

### xyY

```py
>>> Color('red').convert('xyy')
color(--xyy 0.64 0.33 0.21264 / 1)
```

A derivative of this XYZ space, the CIE xyY color space, is often used as a way to graphically present the chromaticity
of colors.

![CMY](https://github.com/facelessuser/coloraide-extras/blob/main/images/xyy.png)

[Learn more](https://en.wikipedia.org/wiki/CIE_1931_color_space#CIE_xy_chromaticity_diagram_and_the_CIE_xyY_color_space).

### CIE 1960 UCS

```py
>>> Color('red').convert('ucs')
color(--ucs 0.27493 0.21264 0.12243 / 1)
```

The CIE 1960 color space ("CIE 1960 UCS", variously expanded Uniform Color Space, Uniform Color Scale, Uniform
Chromaticity Scale, Uniform Chromaticity Space) is another name for the (u, v) chromaticity space devised by David
MacAdam. The color space is implemented using the relation between this space and the XYZ space as coordinates U, V, and
W.

![UCS](https://github.com/facelessuser/coloraide-extras/blob/main/images/ucs.png)

[Learn more](https://en.wikipedia.org/wiki/CIE_1960_color_space)

### CIE 1964 UVW

```py
>>> Color('red').convert('uvw')
color(--uvw 171.8 24.715 52.261 / 1)
```

Wyszecki invented the UVW color space in order to be able to calculate color differences without having to hold the
luminance constant. He defined a lightness index W* by simplifying expressions suggested earlier by Ladd and Pinney,
and Glasser et al.. The chromaticity components U* and V* are defined such that the white point maps to the origin,
as in Adams chromatic valence color spaces.

What's with all the weird negative black values at the bottom? :shrug:

The algorithm is simple enough that it is unlikely that we are wrong, but more the color space was not designed in such
a way to render nicely but to focus mainly on the distancing requirement.

![UVW](https://github.com/facelessuser/coloraide-extras/blob/main/images/uvw.png)

[Learn more](https://en.wikipedia.org/wiki/CIE_1964_color_space).

### HSI

```py
>>> Color('red').convert('hsi')
color(--hsi 0 1 0.33333 / 1)
```

The HSI model is similar to models like HSL and HSV except that it uses I for intensity instead of Lightness or Value.
It does not attempt to "fill" a cylinder by its definition of saturation leading to a very different look when we plot
it.

![HSI](https://github.com/facelessuser/coloraide-extras/blob/main/images/hsi.png)

![HSI Slice](https://github.com/facelessuser/coloraide-extras/blob/main/images/hsi-slice.png)

[Learn more](https://en.wikipedia.org/wiki/HSL_and_HSV#HSI_to_RGB).

### Prismatic

```py
>>> Color('red').convert('prismatic')
color(--prismatic 1 1 0 0 / 1)
```

The Prismatic model introduces a simple transform of the RGB color cube into a light/dark dimension and a 2D hue.  The
hue is a normalized (barycentric)triangle with pure red, green, and blue at the vertices, often called the Maxwell Color
Triangle.  Each cross section of the space is the same barycentric triangle, and the light/dark dimension runs zero to
one for each hue so the whole color volume takes the form of a prism.

![Prismatic](https://github.com/facelessuser/coloraide-extras/blob/main/images/prismatic.png)

[Learn more](http://psgraphics.blogspot.com/2015/10/prismatic-color-model.html).

### Hunter Lab

```py
>>> Color('red').convert('hunter-lab')
color(--hunter-lab 46.113 82.694 28.337 / 1)
```

The Hunter Lab color space, defined in 1948 by Richard S. Hunter, is another color space referred to as "Lab". Like
CIELAB, it was also designed to be computed via simple formulas from the CIEXYZ space, but to be more perceptually
uniform than CIEXYZ. Hunter named his coordinates L, a, and b. The CIE named the coordinates for CIELAB as L*, a*, b* to
distinguish them from Hunter's coordinates.

![Hunter Lab](https://github.com/facelessuser/coloraide-extras/blob/main/images/hunter-lab.png)

[Learn more](https://support.hunterlab.com/hc/en-us/articles/203997095-Hunter-Lab-Color-Scale-an08-96a2).

### IPT

```py
>>> Color('red').convert('ipt')
color(--ipt 0.45616 0.44282 0.62086 / 1)
```

Ebner and Fairchild addressed the issue of non-constant lines of hue in their color space dubbed IPT. The IPT color
space converts D65-adapted XYZ data (XD65, YD65, ZD65) to long-medium-short cone response data (LMS) using an adapted
form of the Hunt–Pointer–Estevez matrix (MHPE(D65)).

The IPT color appearance model excels at providing a formulation for hue where a constant hue value equals a constant
perceived hue independent of the values of lightness and chroma (which is the general ideal for any color appearance
model, but hard to achieve). It is therefore well-suited for gamut mapping implementations.

![IPT](https://github.com/facelessuser/coloraide-extras/blob/main/images/ipt.png)

[Learn more](https://www.researchgate.net/publication/21677980_Development_and_Testing_of_a_Color_Space_IPT_with_Improved_Hue_Uniformity.).

### IgPgTg

```py
>>> Color('red').convert('igpgtg')
color(--igpgtg 0.54834 0.15366 0.43674 / 1)
```

IgPgTg uses the same structure as IPT, an established hue-uniform color space utilized in gamut mapping applications.
While IPT was fit to visual data on the perceived hue, IGPGTG was optimized based on evidence linking the peak
wavelength of Gaussian-shaped light spectra to their perceived hues.

![IgPgTg](https://github.com/facelessuser/coloraide-extras/blob/main/images/igpgtg.png)

[Learn more](https://www.researchgate.net/publication/21677980_Development_and_Testing_of_a_Color_Space_IPT_with_Improved_Hue_Uniformity.).

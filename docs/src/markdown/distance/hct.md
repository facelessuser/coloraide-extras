# HCT

## Description

The HCT color space is a new color space created by Google for Material. It combines the lightness of CIELAB and the
colorfulness (M) and hue (h) from CAM16. CAM16 is a complicated and expensive color space to calculate. HCT adds even
more complexity in order to unite the CIELAB and CAM16 spaces.

One of the applications of HCT is to create tonal palettes, and for us to do so, we needed a way to
[gamut map HCT](../gamut/hct_chroma.md) while preserving the hue and lightness as much as possible, which means we
needed to gamut map in HCT. To do this, we also required a way to tell when we are close to another color, but we didn't
want to convert out of HCT and pay the conversion cost just to determine color distance. So, for this purpose, we
created this distancing method which we will call ∆E~hct~.

The actual implementation simply takes the tone, which is the same as CIELAB's, and converts the hue and colorfulness
to CAM16 UCS _a_ and _b_. We apply the same adjustment to tone that ∆E~2000~ applies to CIELAB's lightness. We won't
make any claims compared to other methods, but it was sufficient for use in the HCT gamut mapping method.

```playground
Color('red').delta_e('blue', method='hct')
```

## Registering

```py
from coloriade import Color as Base
from coloraide_extras.distance.delta_e_hct import DEHCT

class Color(Base): ...

Color.register(DEHCT())
```

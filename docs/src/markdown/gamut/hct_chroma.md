# HCT Chroma

## Description

Google's Material Design uses a new color space called [HCT](../colors/hct.md). It uses the hue and chroma from
[CAM16](../colors/cam16_ucs.md) and the tone/lightness from CIELAB. It is generally meant for SDR color spaces and
models.

HCT Chroma reduces a color's chroma in the HCT color space until the color is just within the color gamut. Tone is
clipped into the SDR range. This helps generally preserve hue and tone (within the SDR range).

When a tone or hue is changed, the chroma may be too high for the new tone and cause the color to be outside the gamut
that the color is intended for (sRGB for Material). Reducing the chroma, specifically in HCT, to get the color back into
gamut with little or no change to the hue and tone is ideal, especially when trying to match Material's tonal pallets.

```playground
c = Color('hct', [266, 62, 50])
tones = [10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 99]
HtmlSteps([c.set('tone', tone).convert('srgb').to_string(hex=True, fit='hct-chroma') for tone in tones])
```

!!! info "Exact Matches"
    
    It is possible that one or more color channels may differ by +/-1 within a range of 0 - 255. This is because our
    implementation implements the color space as described, but we do not implement the implementation 100%.

    Material uses RGB matrices and white point vectors that utilize far less precision than we do. That doesn't make
    their implementation worse or better, but their will be slight difference in the final values. Additionally, the
    Material library uses more coarse steps in things like chroma when converting back to XYZ which most likely allows
    for faster conversions, but not as much fine resolution for great round tripping of values.

## Registering

```py
from coloraide import Color as Base
from coloraide_extras.gamut.fit_hct_chroma import HCTChroma

class Color(Base): ...

Color.register(HCTChroma())
```

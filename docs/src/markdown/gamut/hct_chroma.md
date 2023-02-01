# HCT Chroma

## Description

Google's Material Design uses a new color space called [HCT](../colors/hct.md). It uses the hue and chroma from
[CAM16](../colors/cam16_ucs.md) and the tone/lightness from CIELAB.

When a tone or hue is changed, the chroma may be too high for the new tone and cause the color to be outside the gamut
that the color is intended for (sRGB for Material). Reducing the chroma, specifically in HCT, to get the color back into
gamut with little or no change to the hue and tone is ideal.

One of the applications of HCT is generating tonal palettes. When coupled with ColorAide's [∆E~hct~](../distance/hct.md)
distancing algorithm and the `hct-chroma` gamut mapping algorithm, we can produce tonal palettes just like in Material's
color utilities.

```playground
c = Color('hct', [325, 24, 50])
tones = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100]
HtmlSteps([c.clone().set('tone', tone).convert('srgb').to_string(hex=True, fit='hct-chroma') for tone in tones])
```

Results in our library may be slightly different in some cases compared to the Material color utilities. This is because
we have implemented the library as _described_, we did not port their implementation and so we do not share the exact
same quirks.

Material uses different precision for their transformation matrices between sRGB and XYZ. The exact chroma reduction
algorithms are likely different, though the end result is very similar.

Consider the example below. We've taken the results from Material's tests. We generate the same tonal palettes and
output both as HCT. We can compare which hues stay overall more constant, which chroma gets reduced more than others,
and which hue and tone are less affected by the gamut mapping. Can you tell which is doing the job the _best_?

```playground
def tonal_palette(c):
    tones = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100]
    return [c.clone().set('tone', tone).fit('srgb', method='hct-chroma') for tone in tones]

material1 = ['#000000', '#00006e', '#0001ac',
             '#0000ef', '#343dff', '#5a64ff',
             '#7c84ff', '#9da3ff', '#bec2ff',
             '#e0e0ff', '#f1efff', '#ffffff']
c = Color('blue').convert('hct')
HtmlSteps([x.to_string() for x in tonal_palette(c)])
HtmlSteps([Color(x).convert('hct').to_string() for x in material1])

material2 = ['#000000', '#191a2c', '#2e2f42',
             '#444559', '#5c5d72', '#75758b',
             '#8f8fa6', '#a9a9c1', '#c5c4dd',
             '#e1e0f9', '#f1efff', '#ffffff']
c['chroma'] = 16
HtmlSteps([x.to_string() for x in tonal_palette(c)])
HtmlSteps([Color(x).convert('hct').to_string() for x in material2])
```

## Registering

```py
from coloraide import Color as Base
from coloraide_extras.gamut.fit_hct_chroma import HCTChroma

class Color(Base): ...

Color.register(HCTChroma())
```

# Lstar

## Description

Google's Material Design uses a new color space called [HCT](../colors/hct.md). It uses the hue and chroma from
[CAM16](../colors/cam16_ucs.md) and the tone/lightness from CIELAB. For contrast, they determined using tones that are
"far enough apart" is a good indication of sufficient contrast. Since HCT tone is exactly the same as CIELAB's lightness
(also known as L\*), we've referred to this approach as Lstar.

Lstar's color difference approach to contrast is quite simple, it's literally the difference between two color's
lightness as provided by CIELAB. This method does not care which color is text or background.

$$
L_{max} - L_{min}
$$

```playground
Color('red').contrast('blue', method='lstar')
```

## Registering

```py
from coloraide import Color as Base
from coloraide_extras.contrast.contrast_weber import ContrastLstar

class Color(Base): ...

Color.register(ContrastLstar())
```

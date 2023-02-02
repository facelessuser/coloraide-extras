# CAM16 UCS JMh

<div class="info-container" markdown="1">
!!! info inline end "Properties"

    **Name:** `cam16-ucs-jmh`

    **White Point:** D65

    **Coordinates:**

    Name | Range~\*~
    ---- | -----
    `j`  | [0, 100]
    `m`  | [0, 55]
    `h`  | [0, 360]

    ^\*^ Space is not bound to the range and is only used as a reference to define percentage inputs/outputs in
    relation to the Display P3 color space.

<figure markdown>

![CAM16 UCS JMh](../images/cam16-ucs-jmh.png)

<figcaption markdown>
The sRGB gamut represented within the CAM16 UCS JMh color space.
</figcaption>
</figure>

CAM16 UCS JMh is the defined polar form the [CAM16 UCS](./cam16_ucs.md) color space. It shares the same lightness (J),
but instead of the lab-like components `a` and `b`, it uses colorfulness (M) and hue (h).

[Learn more](https://doi.org/10.1002/col.22131).
</div>

## Channel Aliases

Channels | Aliases
-------- | -------
`j`      | `lightness`
`m`      | `colorfulness`
`h`      | `hue`

## Input/Output

The CAM16 UCS JMh space is not currently supported in the CSS spec, the parsed input and string output formats use the
`#!css-color color()` function format using the custom name `#!css-color --cam16-ucs-jmh`:

```css-color
color(--cam16-ucs-jmh j m h / a)  // Color function
```

The string representation of the color object and the default string output use the
`#!css-color color(--cam16-ucs-jmh j m h / a)` form.

```playground
Color("cam16-ucs-jmh", [59.178, 45.975, 27.393], 1)
Color("cam16-ucs-jmh", [78.364, 30.226, 71.293], 1).to_string()
```

## Registering

```py
from coloraide import Color as Base
from coloraide_extras.spaces.cam16_ucs_jmh import CAM16UCSJMh

class Color(Base): ...

Color.register(CAM16UCSJMh())
```

<style>
.info-container {display: inline-block;}
</style>


## Subclassing

As described in [CAM16 UCS](./cam16_ucs.md), CAM16's transformation of colors is influenced greatly by the viewing
conditions. As CAM16 UCS JMh has its transformation based off of CAM16 UCS, a subclassed `CAM16UCSJMh` should be
associated with a subclassed `CAM16UCS` class using the same viewing conditions. The alternative is to ensure
`CAM16UCSJMh` is translating from XYZ directly instead of from CAM16 UCS Jab.

Additionally, a new `Achromatic` class should be set to the subclassed `CAM16UCSJMh` class. The `Achromatic` object is
responsible for determining if a given JMh color is achromatic or not. When "discounting" is enabled, colorfulness (M)
will be zero or near zero when a color is achromatic, but when disabled, an achromatic color may have a noticeably
higher M depending on how bright the color is.

The `Achromatic` class takes the viewing conditions color space object and can determine when a color is achromatic.
When "discounting" is enabled, it uses a simple threshold, but when "discounting" is not enabled, it maps a spline along
this achromatic response so that ColorAide can properly determine when a color is achromatic, and in turn, interpolate
them in a logical way.

If you are just changing between UCS, SCD, and LCD or even the surround from average to dim or dark, the same parameters
that ColorAide uses out of the box should be sufficient, but if you are changing the adapting luminance, background
luminance, or even the white space, you may need to tune the response and the threshold of the `Achromatic` object.

While not shipped with the library, we do have a tool on the ColorAide repository called `calc_cam16_ucs_jmh_min_m.py`
which is useful for tuning the achromatic response. This is of course a more advanced task, and we are happy to answer
questions related to it over on the repository.

When subclassing, always use a new, unique name, like `jmh-custom` as other features or color spaces may depend on the
`cam16-ucs-jmh` name converting a certain way.

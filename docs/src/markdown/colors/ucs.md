# CIE 1960 UCS

<div class="info-container" markdown="1">
!!! info inline end "Properties"

    **Name:** `ucs`

    **White Point:** D65

    **Coordinates:**

    Name | Range^\*^
    ---- | -----
    `u`  | [0.0, 1.0]
    `v`  | [0.0, 1.0]
    `w`  | [0.0, 1.0]

    ^\*^ current range is quite arbitrary and values can exceed the range, even in an sRGB gamut.

<figure markdown>

![xyY](../images/ucs.png)

<figcaption markdown>
The sRGB gamut represented within the CIE 1960 UCS color space.
</figcaption>
</figure>

The CIE 1960 color space ("CIE 1960 UCS", variously expanded Uniform Color Space, Uniform Color Scale, Uniform
Chromaticity Scale, Uniform Chromaticity Space) is another name for the (u, v) chromaticity space devised by David
MacAdam. The color space is implemented using the relation between this space and the XYZ space as coordinates U, V, and
W.

[Learn more](https://en.wikipedia.org/wiki/CIE_1960_color_space).
</div>

## Channel Aliases

Channels | Aliases
-------- | -------
`u`      |
`v`      |
`w`      |

## Input/Output

The UCS space is not currently supported in the CSS spec, the parsed input and string output formats use the
`#!css-color color()` function format using the custom name `#!css-color --ucs`:

```css-color
color(--ucs u v w / a)  // Color function
```

The string representation of the color object and the default string output use the
`#!css-color color(--ucs u v w / a)` form.

```playground
Color("ucs", [0.27493, 0.21264, 0.12243])
Color("ucs", [0.36462, 0.48173, 0.48122]).to_string()
```

## Registering

```py
from coloraide import Color as Base
from coloraide_extras.spaces.ucs import UCS

class Color(Base): ...

Color.register(UCS())
```

<style>
.info-container {display: inline-block;}
</style>

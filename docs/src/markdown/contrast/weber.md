# Weber Contrast

## Description

Weber contrast is commonly used in cases where small features are present on a large uniform background, i.e., where the
average luminance is approximately equal to the background luminance. The algorithm takes the difference of the
luminance and divides it by the lesser value. This method does not care which color is text or background.

$$
\frac{L_{max} - L_{min}}{L_{min}}
$$

```py play
Color('red').contrast('blue', method='weber')
```

## Registering

```py
from coloraide import Color as Base
from coloraide_extras.contrast.contrast_weber import ContrastWeber

class Color(Base): ...

Color.register(ContrastWeber())
```

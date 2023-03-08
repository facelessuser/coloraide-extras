# Michelson Contrast

## Description

Michelson contrast (also known as the visibility) is commonly used for patterns where both bright and dark features are
equivalent and take up similar fractions of the area (e.g. sine-wave gratings). It measures the relation between the
spread and the sum of the two luminances. This method does not care which color is text or background.

$$
\frac{L_{max} - L_{min}}{L_{max} + L_{min}}
$$

```py play
Color('red').contrast('blue', method='michelson')
```

## Registering

```py
from coloraide import Color as Base
from coloraide_extras.contrast.contrast_weber import ContrastMichelson

class Color(Base): ...

Color.register(ContrastMichelson())
```

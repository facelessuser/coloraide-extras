# Contrast

ColorAide provides WCAG 2.1 color contrast by default, but there are some criticisms related to how well the WCAG 2.1
algorithm performs. This is not a failing of ColorAide, but the contrast algorithm in general.

ColorAide Extras currently provides a few color contrast methods for evaluating other approaches.

Methods                            | Symmetrical         | Description
---------------------------------- | ------------------  | -----------
[`weber`](#weber-contrast)         | :octicons-check-16: | Contrast that uses the measure also referred to as Weber fraction.
[`michelson`](#michelson-contrast) | :octicons-check-16: | Peak-to-peak contrast.

## Weber Contrast

Weber contrast is commonly used in cases where small features are present on a large uniform background, i.e., where the
average luminance is approximately equal to the background luminance. The algorithm takes the difference of the
luminance and divides it by the lesser value.

$$
\frac{L_{max} - L_{min}}{L_{min}}
$$

```playground
Color('red').contrast('blue', method='weber')
```

## Michelson Contrast

Michelson contrast (also known as the visibility) is commonly used for patterns where both bright and dark features are
equivalent and take up similar fractions of the area (e.g. sine-wave gratings). It measures the relation between the
spread and the sum of the two luminances.

$$
\frac{L_{max} - L_{min}}{L_{max} + L_{min}}
$$

```playground
Color('red').contrast('blue', method='weber')
```

# Contrast

ColorAide provides WCAG 2.1 color contrast by default, but there are some criticisms related to how well the WCAG 2.1
algorithm performs. This is not a failing of ColorAide, but the contrast algorithm in general.

ColorAide Extras currently provides a few color contrast methods for evaluating other approaches.

Methods                       | Symmetrical         | Description
----------------------------- | ------------------  | -----------
[`weber`](./weber.md)         | :octicons-check-16: | Contrast that uses the measure also referred to as Weber fraction.
[`michelson`](./michelson.md) | :octicons-check-16: | Peak-to-peak contrast.

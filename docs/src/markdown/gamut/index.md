# Gamut Mapping

ColorAide provides various gamut mapping algorithms, each with certain applications and benefits.

ColorAide Extras currently provides a few experimental gamut mapping approaches.

Methods                         | Description
------------------------------- | -----------
[`hct-chroma`](./hct_chroma.md) | Gamut mapping algorithm that reduces chroma to help preserve hue and lightness in the HCT color space. HDR lightness will be clamped to SDR.

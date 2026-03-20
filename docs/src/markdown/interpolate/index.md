---
icon: lucide/spline
---
# Interpolate

ColorAide Extras provides a few experimental interpolation plugins

Methods                                | Description
-------------------------------------- | -----------
[`spectral`](https://facelessuser.github.io/coloraide/interpolation/#spectral)            | An interpolation plugin that allows for single constant Kubelka-Munk interpolation reflectance curves generated from the sRGB gamut.
[`spectral-continuous`](https://facelessuser.github.io/coloraide/interpolation/#spectral) | A continuous interpolation version of the `spectral` interpolator.

> [!note]
> Spectral mixing has officially been moved to the main ColorAide package. References here are deprecated and will be
> removed in the future. Please use `coloraide.interpolate.spectral.Spectral` and
> `coloraide.interpolate.spectral.SpectralContinuous` instead.

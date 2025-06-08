# Changelog

## 1.11

-   **NEW**: Support Python 3.14.

## 1.10.1

-   **ENHANCE**: Switch to deploying with PyPI's "Trusted Publisher".
-   **ENHANCE**: Update internal algorithm of Spectral mixing to a more efficient approach.

## 1.10

-   **NEW**: Sync types with latest ColorAide and require the latest ColorAide.

## 1.9.3

-   **FIX**: Spectral interpolation should mix residual with the non-luminance-adjusted progress for better out of gamut
    color mixing.

## 1.9.2

-   **FIX**: Fix issues with spectral interpolation.

## 1.9.1

-   **FIX**: Fix issue with how spectral interpolation concentrations are clipped.

## 1.9

-   **NEW**: Drop Python 3.8.
-   **NEW**: Require ColorAide 4.3.
-   **NEW**: Add spectral interpolation that leverages Kubelka-Munk theory for color mixing.

## 1.8

-   **NEW**: Officially support Python 3.13.
-   **NEW**: Require ColorAide 4.0.

## 1.7

-   **NEW**: Officially support Python 3.12.

## 1.6

-   **NEW**: Drop Python 3.7.
-   **NEW**: CIE 1960 UCS moved to official ColorAide repository.

## 1.5

-   **NEW**: All CAM16 related spaces, and distancing plugins moved to official ColorAide.
-   **NEW**: All HCT related spaces, gamut mapping, distancing, and contrast plugins moved to official ColorAide.

## 1.4.2

-   **FIX**: Rework some internals to make tuning achromatic response easier.
-   **FIX**: Simplify ∆E~HCT~ to just simple Euclidean logic against the components.
-   **FIX**: Fix slowness of converting between CAM16 UCS Jab and JMh. JMh will convert from the Jab form instead of XYZ
    directly to make translation between the Jab form and the JMh form much quicker.
-   **FIX**: Calculation of achromatic response in CAM16 UCS JMh should take into account whether discounting is
    enabled.

## 1.4.1

-   **FIX**: Fix ranges on CAM16 UCS JMh.

## 1.4

-   **NEW**: Add CAM16 UCS JMh
-   **NEW**: Allow HCT to work with HDR color spaces.
-   **NEW**: Add ∆E~HCT~ for use in `hct-chroma` gamut mapping.
-   **FIX**: Improve results of `hct-chroma` gamut mapping for better tonal pallets.

## 1.3

-   **NEW**: Add `hct-chroma` gamut mapping algorithm that reduces chroma in HCT until the color is in gamut.
-   **FIX**: When converting from HCT and tone is 0 or 100, shortcut and return white or black.

## 1.2

-   **NEW**: Add HCT color space.
-   **NEW**: Add Lstar contrast (contrast based on lightness difference in the Lab color space).

## 1.1

-   **NEW**: Require stable ColorAide 1.5.
-   **NEW**: Formally support Python 3.11.

## 1.0.1

-   **FIX**: `coloraide_extras.everything.ColorAll` should derive from `coloraide.everything.ColorAll`, not
    `coloraide.Color`.
-   **FIX**: Handle divide by zero case for Weber contrast by setting a more reasonable max.

## 1.0.post1

-   **FIX**: Remove beta notices from documentation.

## 1.0

-   **NEW**: Update to support the official ColorAide stable release. Move to a "stable" release for ColorAide Extras.

## 1.0rc1

-   **NEW**: Move the `Color` object which contains **all** plugins to `coloraide_extras.everything.ColorAll`. This will
    prevent instantiating things that some users may not care about.
-   **NEW**: Plugins are no longer available root of package, but must be imported from their location:
    `coloraide_extras.<plugin_type>.<space>.<class>`.
-   **FIX**: Clamp luminance in Michelson and Weber contrast plugins to zero if negative luminance.
-   **FIX**: Adjust some color space ranges to be more reasonable.

## 1.0b1

-   **NEW**: Add support for new ColorAide 1.0 Beta.
-   **NEW**: All previous color spaces except UCS and UVW have been moved to ColorAide 1.0 Beta.
-   **NEW**: Added CAM16 UCS, CAM16 LCD, and CAM16 SCD and an associated `cam16` ∆E.
-   **NEW**: Added Weber contrast and Michelson contrast.

## 0.5.1

-   **FIX**: Fix Hunter Lab values.

## 0.5.0

-   **NEW**: Update to support ColorAide 0.16.0 changes.

## 0.4.0

-   **NEW**: Added oRGB color space.

## 0.3.0

-   **NEW**: Updated to work with ColorAide 0.15.0 (now the required minimum) as there were substantial changes.
-   **NEW**: Added support for RLAB color space.

## 0.2.0

-   **NEW**: Updated to work with latest ColorAide.
-   **FIX**: IPT and IgPgTg mismatched channel association (`p` <=> `t`). This also broke round trip conversions.

## 0.1.2

-   **FIX**: Fix UVW calculation when `u = v = w = 0`.

## 0.1.1

-   **FIX**: Fix some divide by zero cases in some of the color spaces.
-   **FIX**: Fix CMYK logic.

## 0.1.0

-   **NEW**: Initial release.

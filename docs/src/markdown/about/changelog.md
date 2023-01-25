# Changelog

## 1.2

- **NEW**: Add HCT color space.
- **NEW**: Add Lstar contrast (contrast based on lightness difference in the Lab color space).

## 1.1

- **NEW**: Require stable ColorAide 1.5.
- **NEW**: Formally support Python 3.11.

## 1.0.1

- **FIX**: `coloraide_extras.everything.ColorAll` should derive from `coloraide.everything.ColorAll`, not
  `coloraide.Color`.
- **FIX**: Handle divide by zero case for Weber contrast by setting a more reasonable max.

## 1.0.post1

- **FIX**: Remove beta notices from documentation.

## 1.0

- **NEW**: Update to support the official ColorAide stable release. Move to a "stable" release for ColorAide Extras.

## 1.0rc1

- **NEW**: Move the `Color` object which contains **all** plugins to `coloraide_extras.everything.ColorAll`. This will
  prevent instantiating things that some users may not care about.
- **NEW**: Plugins are no longer available root of package, but must be imported from their location:
  `coloraide_extras.<plugin_type>.<space>.<class>`.
- **FIX**: Clamp luminance in Michelson and Weber contrast plugins to zero if negative luminance.
- **FIX**: Adjust some color space ranges to be more reasonable.

## 1.0b1

- **NEW**: Add support for new ColorAide 1.0 Beta.
- **NEW**: All previous color spaces except UCS and UVW have been moved to ColorAide 1.0 Beta.
- **NEW**: Added CAM16 UCS, CAM16 LCD, and CAM16 SCD and an associated `cam16` ∆E.
- **NEW**: Added Weber contrast and Michelson contrast.

## 0.5.1

- **FIX**: Fix Hunter Lab values.

## 0.5.0

- **NEW**: Update to support ColorAide 0.16.0 changes.

## 0.4.0

- **NEW**: Added oRGB color space.

## 0.3.0

- **NEW**: Updated to work with ColorAide 0.15.0 (now the required minimum) as there were substantial changes.
- **NEW**: Added support for RLAB color space.

## 0.2.0

- **NEW**: Updated to work with latest ColorAide.
- **FIX**: IPT and IgPgTg mismatched channel association (`p` <=> `t`). This also broke round trip conversions.

## 0.1.2

- **FIX**: Fix UVW calculation when `u = v = w = 0`.

## 0.1.1

- **FIX**: Fix some divide by zero cases in some of the color spaces.
- **FIX**: Fix CMYK logic.

## 0.1.0

- **NEW**: Initial release.

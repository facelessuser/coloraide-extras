# Changelog

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

# Changelog

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

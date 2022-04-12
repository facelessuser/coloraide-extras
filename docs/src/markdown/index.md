# Introduction

!!! warning "Currently a Prerelease"
    Like [ColorAide](https://github.com/facelessuser/coloraide), ColorAide Extras is very usable and out of the alpha
    stage, but it is currently in a prerelease state. This simply means that the API of ColorAide is still in flux to
    some degree and could affect this package.

ColorAide Extras is an add-on pack containing various plugins for [ColorAide](https://github.com/facelessuser/coloraide).
ColorAide only ships with a select number of color spaces, ∆E methods, and gamut mapping alternatives. ColorAide Extras
allows us to offer an additional number of uncommon and/or experimental set of color spaces and other plugins.

## Installation

The recommended way to install ColorAide Extras is to use `pip`:

```console
$ pip install coloraide_extras
```

## Usage

If you want access to all the color spaces for both ColorAide and ColorAide Extras, simply import `Color` from
`coloraide_extras` instead of `coloraide`:

```playground
from coloraide_extras import Color
Color('color(--hunter-lab 46.113 82.694 28.337 / 1)')
```

If you'd like to only grab a few, simply subclass `Color` from `coloraide` and register the additional plugins that you
desire:

```playground
from coloraide import Color as Base
from coloraide_extras.spaces.hunter_lab import HunterLab
class Color(Base): ...
Color.register(HunterLab)
Color('red').convert('hunter-lab')
```

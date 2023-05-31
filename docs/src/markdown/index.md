# Introduction

/// warning | Experimental
Plugins provided by ColorAide Extras is essentially an experimental playground. Regardless of how polished a given
plugin may seem, they should be considered experimental.
///

## Overview

ColorAide Extras is an add-on pack containing various plugins for [ColorAide](https://github.com/facelessuser/coloraide).
The idea behind ColorAide Extras is to provide an environment for experimental color spaces, ∆E methods, and other
plugins.

## Installation

The recommended way to install ColorAide Extras is to use `pip`:

```console
$ pip install coloraide_extras
```

## Usage

Normally, it is advisable to only cherry pick color spaces you need. Rarely do people need every color space. This can
be done simply by registering the color spaces you'd like.

```py play
from coloraide import Color as Base
from coloraide_extras.spaces.uvw import UVW
class Color(Base): ...
Color.register(UVW())
Color('red').convert('uvw')
```

But, if you want access to all the color spaces for both ColorAide and ColorAide Extras, simply import `ColorAll` from
`coloraide_extras.everything` instead of `coloraide`:


```py play
from coloraide_extras.everything import ColorAll as Color
Color('color(--uvw 171.8 24.715 52.261 / 1)')
```

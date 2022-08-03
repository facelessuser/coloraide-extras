# Introduction

!!! warning "Experimental"
    Plugins provided by ColorAide Extras is essentially an experimental playground. Regardless of how polished a given
    plugin may seem, they should be considered experimental.

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

```playground
from coloraide import Color as Base
from coloraide_extras.spaces.ucs import UCS
class Color(Base): ...
Color.register(UCS())
Color('red').convert('ucs')
```

But, if you want access to all the color spaces for both ColorAide and ColorAide Extras, simply import `ColorAll` from
`coloraide_extras.everything` instead of `coloraide`:


```playground
from coloraide_extras.everything import ColorAll as Color
Color('color(--ucs 0.27493 0.21264 0.12243 / 1)')
```

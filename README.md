[![Donate via PayPal][donate-image]][donate-link]
[![Discord][discord-image]][discord-link]
[![Build][github-ci-image]][github-ci-link]
[![Coverage Status][codecov-image]][codecov-link]
[![PyPI Version][pypi-image]][pypi-link]
[![PyPI Downloads][pypi-down]][pypi-link]
[![PyPI - Python Version][python-image]][pypi-link]
![License][license-image-mit]

# ColorAide Extras

> **This is still a work in progress.**
>
> Like ColorAide, ColorAide Extras is very usable and out of the alpha stage, but it is currently in a prerelease state.
> This simply means that the API of ColorAide is still in flux to some degree and could affect this package.

## Overview

ColorAide Extras is an add-on pack containing various plugins for [ColorAide](https://github.com/facelessuser/coloraide).
ColorAide only ships with a select number of color spaces, ∆E methods, and gamut mapping alternatives. ColorAide Extras
allows us to offer an additional number of uncommon and/or experimental set of color spaces and other plugins.

If you want access to all the color spaces for both ColorAide and ColorAide Extras, simply import `Color` from
`coloraide_extras` instead of `coloraide`:

```python
>>> from coloraide_extras import Color
>>> Color('color(--hunter-lab 46.113 82.694 28.337 / 1)')
color(--hunter-lab 46.113 82.694 28.337 / 1)
```

If you'd like to only grab a few, simply subclass `Color` from `coloraide` and register the additional plugins that you
desire:

```python
>>> from coloraide import Color as Base
>>> from coloraide_extras.spaces.hunter_lab import HunterLab
>>> class Color(Base): ...
... 
>>> Color.register(HunterLab)
>>> Color('red').convert('hunter-lab')
color(--hunter-lab 46.113 82.694 28.337 / 1)
```

# Documentation

https://facelessuser.github.io/coloraide-extras

## License

MIT

[github-ci-image]: https://github.com/facelessuser/coloraide-extras/workflows/build/badge.svg?branch=main&event=push
[github-ci-link]: https://github.com/facelessuser/coloraide-extras/actions?query=workflow%3Abuild+branch%3Amaster
[discord-image]: https://img.shields.io/discord/678289859768745989?logo=discord&logoColor=aaaaaa&color=mediumpurple&labelColor=333333
[discord-link]:https://discord.gg/TWs8Tgr
[codecov-image]: https://img.shields.io/codecov/c/github/facelessuser/coloraide-extras/main.svg?logo=codecov&logoColor=aaaaaa&labelColor=333333
[codecov-link]: https://codecov.io/github/facelessuser/coloraide-extras
[pypi-image]: https://img.shields.io/pypi/v/coloraide-extras.svg?logo=pypi&logoColor=aaaaaa&labelColor=333333
[pypi-down]: https://img.shields.io/pypi/dm/coloraide-extras.svg?logo=pypi&logoColor=aaaaaa&labelColor=333333
[pypi-link]: https://pypi.python.org/pypi/coloraide-extras
[python-image]: https://img.shields.io/pypi/pyversions/coloraide_extras?logo=python&logoColor=aaaaaa&labelColor=333333
[license-image-mit]: https://img.shields.io/badge/license-MIT-blue.svg?labelColor=333333
[donate-image]: https://img.shields.io/badge/Donate-PayPal-3fabd1?logo=paypal
[donate-link]: https://www.paypal.me/facelessuser

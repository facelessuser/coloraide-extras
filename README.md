[![Donate via PayPal][donate-image]][donate-link]
[![Discord][discord-image]][discord-link]
[![Build][github-ci-image]][github-ci-link]
[![Coverage Status][codecov-image]][codecov-link]
[![PyPI Version][pypi-image]][pypi-link]
[![PyPI Downloads][pypi-down]][pypi-link]
[![PyPI - Python Version][python-image]][pypi-link]
![License][license-image-mit]

# ColorAide Extras

> **Since [ColorAide](https://github.com/facelessuser/coloraide) is now in beta, ColorAide Extra is also in beta!**

## Overview

ColorAide Extras is an add-on pack containing various plugins for [ColorAide](https://github.com/facelessuser/coloraide).
The idea behind ColorAide Extras is to provide an environment for experimental color spaces, ∆E methods, and other
plugins.

Normally, it is advisable to only cherry pick color spaces you need. Rarely do people need every color space. This can
be done simply by registering the color spaces you'd like.

```python
>>> from coloraide import Color as Base
>>> from coloraide_extras.spaces.ucs import UCS
>>> class Color(Base): ...
...
>>> Color.register(UCS)
>>> Color('red').convert('ucs')
color(--ucs 0.27493 0.21264 0.12243 / 1)
```

But, if you want access to all the color spaces for both ColorAide and ColorAide Extras, simply import `Color` from
`coloraide_extras` instead of `coloraide`:

```python
>>> from coloraide_extras.everything import ColorAll as Color
>>> Color('color(--ucs 0.27493 0.21264 0.12243 / 1)')
color(--ucs 0.27493 0.21264 0.12243 / 1)
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

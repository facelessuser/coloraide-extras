"""Test interpolation plugins."""
import unittest
from coloraide_extras.everything import ColorAll as Color
from coloraide import NaN
from . import util


class TestSpectral(util.ColorAsserts, unittest.TestCase):
    """Test spectral color mixing."""

    def test_blue_yellow(self):
        """Test yellow and blue mixing."""

        c1 = Color('#002185')
        c2 = Color('#FCD200')
        expected = [
            Color('color(xyz-d65 0.04777 0.02781 0.22476 / 1)'),
            Color('color(xyz-d65 0.02702 0.03256 0.0952 / 1)'),
            Color('color(xyz-d65 0.03708 0.06349 0.07065 / 1)'),
            Color('color(xyz-d65 0.07141 0.12697 0.07348 / 1)'),
            Color('color(xyz-d65 0.13374 0.22374 0.08054 / 1)'),
            Color('color(xyz-d65 0.22802 0.34531 0.08724 / 1)'),
            Color('color(xyz-d65 0.35287 0.47483 0.09216 / 1)'),
            Color('color(xyz-d65 0.49749 0.59023 0.09487 / 1)'),
            Color('color(xyz-d65 0.6319 0.6679 0.09564 / 1)')
        ]
        for a, b in zip(Color.steps([c1, c2], method='spectral', steps=9), expected):
            self.assertColorEqual(a, b)

    def test_mix_nan(self):
        """Test mixing with NaN."""

        red = Color('red')
        green = Color('green')
        blue = Color('blue')
        green.convert('xyz-d65', in_place=True).set('y', NaN)

        self.assertColorEqual(
            Color.interpolate([red, green, blue], method='spectral')(0.25),
            Color('color(xyz-d65 0.04012 0.03909 0.00367)')
        )

        self.assertColorEqual(
            Color.interpolate([red, green, blue], method='spectral')(0.75),
            Color('color(xyz-d65 0.02697 0.03463 0.0467)')
        )

        red.convert('xyz-d65', in_place=True).set('y', NaN)
        blue.convert('xyz-d65', in_place=True).set('y', NaN)

        self.assertColorEqual(
            Color.interpolate([red, green], method='spectral')(0.5),
            Color('color(xyz-d65 0.13635 -0.05537 0.0189)')
        )

    def test_mix_black(self):
        """Mix with black."""

        self.assertColorEqual(
            Color('black').mix('red', method='spectral'), Color('color(xyz-d65 0.08223 0.04839 0.01747)')
        )
        self.assertColorEqual(
            Color('red').mix('black', method='spectral'), Color('color(xyz-d65 0.08223 0.04839 0.01747)')
        )

    def test_bad_color_space(self):
        """Spectral will only mix in XYZ."""

        with self.assertRaises(ValueError):
            Color('red').mix('blue', method='spectral', space='lab')

    def test_easing(self):
        """Test easing functions."""

        self.assertColorEqual(
            Color.interpolate(
                ['red', Color('blue').set('alpha', 0)],
                progress=lambda t: 0,
                method='spectral'
            )(1),
            Color('color(xyz-d65 0.41239 0.21264 0.01933 / 1)')
        )

    def test_easing_all(self):
        """Test easing all channels."""

        self.assertColorEqual(
            Color.interpolate(
                ['red', Color('blue').set('alpha', 0)],
                progress={
                    'all': lambda t: 0,
                },
                method='spectral'
            )(1),
            Color('color(xyz-d65 0.41239 0.21264 0.01933 / 1)')
        )

    def test_easing_channel(self):
        """Test easing specific channels does not work."""

        self.assertColorEqual(
            Color.interpolate(
                ['red', Color('blue').set('alpha', 0.5)],
                progress={
                    'x': lambda t: 0,
                },
                method='spectral'
            )(1),
            Color('color(xyz-d65 0.18048 0.07219 0.95053 / 0.5)')
        )

    def test_easing_alpha(self):
        """Test easing alpha does work."""

        self.assertColorEqual(
            Color.interpolate(
                ['red', Color('blue').set('alpha', 0.5)],
                progress={
                    'alpha': lambda t: 0,
                },
                method='spectral'
            )(1),
            Color('color(xyz-d65 0.09024 0.0361 0.47527 / 1)')
        )

    def test_blue_yellow_continuous(self):
        """Test yellow and blue mixing."""

        c1 = Color('#002185')
        c2 = Color('#FCD200')
        expected = [
            Color('color(xyz-d65 0.04777 0.02781 0.22476 / 1)'),
            Color('color(xyz-d65 0.02702 0.03256 0.0952 / 1)'),
            Color('color(xyz-d65 0.03708 0.06349 0.07065 / 1)'),
            Color('color(xyz-d65 0.07141 0.12697 0.07348 / 1)'),
            Color('color(xyz-d65 0.13374 0.22374 0.08054 / 1)'),
            Color('color(xyz-d65 0.22802 0.34531 0.08724 / 1)'),
            Color('color(xyz-d65 0.35287 0.47483 0.09216 / 1)'),
            Color('color(xyz-d65 0.49749 0.59023 0.09487 / 1)'),
            Color('color(xyz-d65 0.6319 0.6679 0.09564 / 1)')
        ]
        for a, b in zip(Color.steps([c1, c2], method='spectral-continuous', steps=9), expected):
            self.assertColorEqual(a, b)

    def test_mix_nan_continuous(self):
        """Test mixing with NaN in continuous mode."""

        red = Color('red')
        green = Color('green')
        blue = Color('blue')
        green.convert('xyz-d65', in_place=True).set('y', NaN)

        self.assertColorEqual(
            Color.interpolate([red, green, blue], method='spectral-continuous')(0.25),
            Color('color(xyz-d65 0.0622 0.04615 0.01112)')
        )

        self.assertColorEqual(
            Color.interpolate([red, green, blue], method='spectral-continuous')(0.75),
            Color('color(xyz-d65 0.02667 0.05355 0.02985)')
        )

    def test_bad_color_space_continuous(self):
        """Spectral continuous will only mix in XYZ."""

        with self.assertRaises(ValueError):
            Color('red').mix('blue', method='spectral-continuous', space='lab')

    def test_easing_continuous(self):
        """Test easing functions."""

        self.assertColorEqual(
            Color.interpolate(
                ['red', Color('blue').set('alpha', 0)],
                progress=lambda t: 0,
                method='spectral-continuous'
            )(1),
            Color('color(xyz-d65 0.41239 0.21264 0.01933 / 1)')
        )

    def test_easing_all_continuous(self):
        """Test easing all channels."""

        self.assertColorEqual(
            Color.interpolate(
                ['red', Color('blue').set('alpha', 0)],
                progress={
                    'all': lambda t: 0,
                },
                method='spectral-continuous'
            )(1),
            Color('color(xyz-d65 0.41239 0.21264 0.01933 / 1)')
        )

    def test_easing_channel_continuous(self):
        """Test easing specific channels does not work."""

        self.assertColorEqual(
            Color.interpolate(
                ['red', Color('blue').set('alpha', 0.5)],
                progress={
                    'x': lambda t: 0,
                },
                method='spectral-continuous'
            )(1),
            Color('color(xyz-d65 0.18048 0.07219 0.95053 / 0.5)')
        )

    def test_easing_alpha_continuous(self):
        """Test easing alpha does work."""

        self.assertColorEqual(
            Color.interpolate(
                ['red', Color('blue').set('alpha', 0.5)],
                progress={
                    'alpha': lambda t: 0,
                },
                method='spectral-continuous'
            )(1),
            Color('color(xyz-d65 0.09024 0.0361 0.47527 / 1)')
        )


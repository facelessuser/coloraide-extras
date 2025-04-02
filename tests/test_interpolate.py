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
            Color('color(xyz-d65 0.02667 0.03298 0.0951 / 1)'),
            Color('color(xyz-d65 0.03708 0.06387 0.07248 / 1)'),
            Color('color(xyz-d65 0.07117 0.12699 0.07519 / 1)'),
            Color('color(xyz-d65 0.13265 0.22305 0.08176 / 1)'),
            Color('color(xyz-d65 0.22548 0.34363 0.08795 / 1)'),
            Color('color(xyz-d65 0.34991 0.47284 0.09246 / 1)'),
            Color('color(xyz-d65 0.49784 0.59012 0.09493 / 1)'),
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
            Color('color(xyz-d65 0.02701 0.03438 0.04685)')
        )

        red.convert('xyz-d65', in_place=True).set('y', NaN)
        blue.convert('xyz-d65', in_place=True).set('y', NaN)

        self.assertColorEqual(
            Color.interpolate([red, green], method='spectral')(0.5),
            Color('color(xyz-d65 0.12966 -0.05897 0.01868)')
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
            Color('color(xyz-d65 0.02667 0.03298 0.0951 / 1)'),
            Color('color(xyz-d65 0.03708 0.06387 0.07248 / 1)'),
            Color('color(xyz-d65 0.07117 0.12699 0.07519 / 1)'),
            Color('color(xyz-d65 0.13265 0.22305 0.08176 / 1)'),
            Color('color(xyz-d65 0.22548 0.34363 0.08795 / 1)'),
            Color('color(xyz-d65 0.34991 0.47284 0.09246 / 1)'),
            Color('color(xyz-d65 0.49784 0.59012 0.09493 / 1)'),
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
            Color('color(xyz-d65 0.06172 0.046 0.011)')
        )

        self.assertColorEqual(
            Color.interpolate([red, green, blue], method='spectral-continuous')(0.75),
            Color('color(xyz-d65 0.02659 0.05347 0.0299)')
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


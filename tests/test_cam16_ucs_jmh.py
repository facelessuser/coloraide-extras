"""Test CAM16 UCS JMh."""
import unittest
from . import util
from coloraide_extras.everything import ColorAll as Color, NaN
import pytest


class TestCAM16UCSJMh(util.ColorAssertsPyTest):
    """Test JMh."""

    COLORS = [
        ('red', 'color(--cam16-ucs-jmh 59.178 45.975 27.393)'),
        ('orange', 'color(--cam16-ucs-jmh 78.364 30.226 71.293)'),
        ('yellow', 'color(--cam16-ucs-jmh 96.802 35.423 111.15)'),
        ('green', 'color(--cam16-ucs-jmh 46.661 33.803 142.3)'),
        ('blue', 'color(--cam16-ucs-jmh 36.252 38.828 282.75)'),
        ('indigo', 'color(--cam16-ucs-jmh 24.524 30.11 310.9)'),
        ('violet', 'color(--cam16-ucs-jmh 74.738 31.837 331.39)'),
        ('white', 'color(--cam16-ucs-jmh 100 2.1817 0)'),
        ('gray', 'color(--cam16-ucs-jmh 56.23 1.443 0)'),
        ('black', 'color(--cam16-ucs-jmh 0 0 0)')
    ]

    @pytest.mark.parametrize('color1,color2', COLORS)
    def test_colors(self, color1, color2):
        """Test colors."""

        self.assertColorEqual(Color(color1).convert('cam16-ucs-jmh'), Color(color2))


class TestJMhPoperties(util.ColorAsserts, unittest.TestCase):
    """Test JMh properties."""

    def test_names(self):
        """Test LCh-ish names."""

        self.assertEqual(Color('color(--cam16-ucs-jmh 70 75.504 97.139)')._space.lchish_names(), ('j', 'm', 'h'))

    def test_j(self):
        """Test `j`."""

        c = Color('color(--cam16-ucs-jmh 70 75.504 97.139)')
        self.assertEqual(c['j'], 70)
        c['j'] = 270
        self.assertEqual(c['j'], 270)

    def test_m(self):
        """Test `m`."""

        c = Color('color(--cam16-ucs-jmh 70 75.504 97.139)')
        self.assertEqual(c['m'], 75.504)
        c['m'] = 30
        self.assertEqual(c['m'], 30)

    def test_t(self):
        """Test `t`."""

        c = Color('color(--cam16-ucs-jmh 70 75.504 97.139)')
        self.assertEqual(c['h'], 97.139)
        c['h'] = 50
        self.assertEqual(c['h'], 50)

    def test_alpha(self):
        """Test `alpha`."""

        c = Color('color(--cam16-ucs-jmh 70 75.504 97.139)')
        self.assertEqual(c['alpha'], 1)
        c['alpha'] = 0.5
        self.assertEqual(c['alpha'], 0.5)


class TestNull(util.ColorAsserts, unittest.TestCase):
    """Test Null cases."""

    def test_null_input(self):
        """Test null input."""

        c = Color('cam16-ucs-jmh', [30, 20, NaN], 1)
        self.assertTrue(c.is_nan('hue'))

    def test_none_input(self):
        """Test `none` null."""

        c = Color('color(--cam16-ucs-jmh 30 20 none / 1)')
        self.assertTrue(c.is_nan('hue'))

    def test_null_normalization_min_chroma(self):
        """Test minimum saturation."""

        c = Color('color(--cam16-ucs-jmh 1 0.05 90 / 1)').normalize()
        self.assertTrue(c.is_nan('hue'))

        c = Color('color(--cam16-ucs-jmh 7 0.05 30)').normalize()
        self.assertTrue(c.is_nan('hue'))

        c = Color('color(--cam16-ucs-jmh 500 0.05 30)').normalize()
        self.assertTrue(c.is_nan('hue'))

    def test_achromatic_hue(self):
        """Test that all RGB-ish colors convert to JMh with a null hue."""

        for space in ('srgb', 'display-p3', 'rec2020', 'a98-rgb', 'prophoto-rgb'):
            for x in range(0, 256):
                color = Color('color({space} {num:f} {num:f} {num:f})'.format(space=space, num=x / 255))
                color2 = color.convert('cam16-ucs-jmh')
                self.assertTrue(color2.is_nan('hue'))

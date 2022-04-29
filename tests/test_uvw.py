"""Test UVW 1964."""
import unittest
from . import util
from coloraide_extras import Color
import pytest


class TestUVW(util.ColorAssertsPyTest):
    """Test UVW 1964."""

    COLORS = [
        ('red', 'color(--uvw 171.8 24.715 52.261)'),
        ('orange', 'color(--uvw 73.871 48.705 73.965)'),
        ('yellow', 'color(--uvw 7.628 70.501 96.177)'),
        ('green', 'color(--uvw -42.842 36.934 45.249)'),
        ('blue', 'color(--uvw -9.1161 -84.255 31.317)'),
        ('indigo', 'color(--uvw 9.5941 -38.921 19.483)'),
        ('violet', 'color(--uvw 51.118 -44.069 68.724)'),
        ('white', 'color(--uvw 0 0 99.04)'),
        ('gray', 'color(--uvw 0 0 52.609)'),
        ('black', 'color(--uvw 0 0 -17)')
    ]

    @pytest.mark.parametrize('color1,color2', COLORS)
    def test_uvw_colors(self, color1, color2):
        """Test colors."""

        self.assertColorEqual(Color(color1).convert('uvw'), Color(color2))


class TestUVWPoperties(util.ColorAsserts, unittest.TestCase):
    """Test UVW."""

    def test_u(self):
        """Test `u`."""

        c = Color('color(--uvw 7.628 70.501 96.177)')
        self.assertEqual(c['u'], 7.628)
        c['u'] = 0.2
        self.assertEqual(c['u'], 0.2)

    def test_v(self):
        """Test `v`."""

        c = Color('color(--uvw 7.628 70.501 96.177)')
        self.assertEqual(c['v'], 70.501)
        c['v'] = 0.1
        self.assertEqual(c['v'], 0.1)

    def test_w(self):
        """Test `w`."""

        c = Color('color(--uvw 7.628 70.501 96.177)')
        self.assertEqual(c['w'], 96.177)
        c['w'] = 0.1
        self.assertEqual(c['w'], 0.1)

    def test_alpha(self):
        """Test `alpha`."""

        c = Color('color(--uvw 7.628 70.501 96.177)')
        self.assertEqual(c['alpha'], 1)
        c['alpha'] = 0.5
        self.assertEqual(c['alpha'], 0.5)

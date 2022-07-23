"""Test UCS 1960."""
import unittest
from . import util
from coloraide_extras.everything import ColorAll as Color
import pytest


class TestUCS(util.ColorAssertsPyTest):
    """Test UCS 1960."""

    COLORS = [
        ('red', 'color(--ucs 0.27493 0.21264 0.12243)'),
        ('orange', 'color(--ucs 0.36462 0.48173 0.48122)'),
        ('yellow', 'color(--ucs 0.51332 0.92781 1.076)'),
        ('green', 'color(--ucs 0.05146 0.15438 0.20584)'),
        ('blue', 'color(--ucs 0.12032 0.07219 0.49331)'),
        ('indigo', 'color(--ucs 0.0462 0.03108 0.11874)'),
        ('violet', 'color(--ucs 0.39115 0.40317 0.73932)'),
        ('white', 'color(--ucs 0.63364 1 1.5693)'),
        ('gray', 'color(--ucs 0.13678 0.21586 0.33875)'),
        ('black', 'color(--ucs 0 0 0)')
    ]

    @pytest.mark.parametrize('color1,color2', COLORS)
    def test_ucs_colors(self, color1, color2):
        """Test colors."""

        self.assertColorEqual(Color(color1).convert('ucs'), Color(color2))


class TestUCSPoperties(util.ColorAsserts, unittest.TestCase):
    """Test UCS."""

    def test_u(self):
        """Test `u`."""

        c = Color('color(--ucs 0.51332 0.92781 1.076)')
        self.assertEqual(c['u'], 0.51332)
        c['u'] = 0.2
        self.assertEqual(c['u'], 0.2)

    def test_v(self):
        """Test `v`."""

        c = Color('color(--ucs 0.51332 0.92781 1.076)')
        self.assertEqual(c['v'], 0.92781)
        c['v'] = 0.1
        self.assertEqual(c['v'], 0.1)

    def test_w(self):
        """Test `w`."""

        c = Color('color(--ucs 0.51332 0.92781 1.076)')
        self.assertEqual(c['w'], 1.076)
        c['w'] = 0.1
        self.assertEqual(c['w'], 0.1)

    def test_alpha(self):
        """Test `alpha`."""

        c = Color('color(--ucs 0.51332 0.92781 1.076)')
        self.assertEqual(c['alpha'], 1)
        c['alpha'] = 0.5
        self.assertEqual(c['alpha'], 0.5)

"""Test Hunter Lab."""
import unittest
from . import util
from coloraide_extras import Color
import pytest


class TestHunterLab(util.ColorAssertsPyTest):
    """Test Hunter Lab."""

    COLORS = [
        ('red', 'color(--hunter-lab 46.113 82.695 28.336)'),
        ('orange', 'color(--hunter-lab 69.407 23.272 40.842)'),
        ('yellow', 'color(--hunter-lab 96.323 -21.06 55.727)'),
        ('green', 'color(--hunter-lab 39.291 -32.095 22.311)'),
        ('blue', 'color(--hunter-lab 26.869 75.499 -199.78)'),
        ('indigo', 'color(--hunter-lab 17.629 40.907 -62.756)'),
        ('violet', 'color(--hunter-lab 63.496 58.124 -40.407)'),
        ('white', 'color(--hunter-lab 100 0 0)'),
        ('gray', 'color(--hunter-lab 46.461 0 0)'),
        ('black', 'color(--hunter-lab 0 0 0)')
    ]

    @pytest.mark.parametrize('color1,color2', COLORS)
    def test_hunter_lab_colors(self, color1, color2):
        """Test colors."""

        self.assertColorEqual(Color(color1).convert('hunter-lab'), Color(color2))


class TestHunterLabPoperties(util.ColorAsserts, unittest.TestCase):
    """Test Hunter Lab."""

    def test_l(self):
        """Test `l`."""

        c = Color('color(--hunter-lab 96.323 -21.06 55.728)')
        self.assertEqual(c['l'], 96.323)
        c['l'] = 0.2
        self.assertEqual(c['l'], 0.2)

    def test_a(self):
        """Test `a`."""

        c = Color('color(--hunter-lab 96.323 -21.06 55.728)')
        self.assertEqual(c['a'], -21.06)
        c['a'] = 0.1
        self.assertEqual(c['a'], 0.1)

    def test_b(self):
        """Test `b`."""

        c = Color('color(--hunter-lab 96.323 -21.06 55.728)')
        self.assertEqual(c['b'], 55.728)
        c['b'] = 0.1
        self.assertEqual(c['b'], 0.1)

    def test_alpha(self):
        """Test `alpha`."""

        c = Color('color(--hunter-lab 96.323 -21.06 55.728)')
        self.assertEqual(c['alpha'], 1)
        c['alpha'] = 0.5
        self.assertEqual(c['alpha'], 0.5)

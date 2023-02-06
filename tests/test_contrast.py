"""Test contrast."""
import unittest
from coloraide_extras.everything import ColorAll as Color
from . import util


class TestContrastWeber(util.ColorAsserts, unittest.TestCase):
    """Test Weber contrast ratio specifics."""

    def test_contrast_same(self):
        """Test contrast of to same colors."""

        self.assertEqual(Color('blue').contrast('blue', method='weber'), 0)

    def test_contrast_zero_luminance(self):
        """Test contrast of two blacks (divide by zero)."""

        self.assertEqual(Color('black').contrast('black', method='weber'), 50000)

    def test_contrast_bigger(self):
        """Test greater contrast."""

        self.assertCompare(Color('white').contrast('blue', method='weber'), 12.85189)

    def test_symmetry(self):
        """Test symmetry."""

        self.assertEqual(
            Color('white').contrast('blue', method='weber'),
            Color('blue').contrast('white', method='weber')
        )


class TestContrastMichelson(util.ColorAsserts, unittest.TestCase):
    """Test Michelson contrast ratio specifics."""

    def test_contrast_same(self):
        """Test contrast of two same colors."""

        self.assertEqual(Color('blue').contrast('blue', method='michelson'), 0)

    def test_contrast_zero(self):
        """Test contrast of two black colors (divide by zero)."""

        self.assertEqual(Color('black').contrast('black', method='michelson'), 0)

    def test_contrast_bigger(self):
        """Test greater contrast."""

        self.assertCompare(Color('white').contrast('blue', method='michelson'), 0.86534)

    def test_symmetry(self):
        """Test symmetry."""

        self.assertEqual(
            Color('white').contrast('blue', method='michelson'),
            Color('blue').contrast('white', method='michelson')
        )

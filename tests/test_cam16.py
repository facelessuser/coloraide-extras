"""Test CAM16 UCS."""
import unittest
from . import util
from coloraide_extras.everything import ColorAll as Color
from coloraide_extras.spaces.cam16_ucs import cam16_to_xyz_d65, CAM16UCS
import pytest
from collections import namedtuple

CAM16Coords = namedtuple("CAM16Coords", "J C h s Q M H")


class TestCAM16CAM16UCS(util.ColorAssertsPyTest):
    """Test CAM16 UCS."""

    COLORS = [
        ('red', 'color(--cam16-ucs 59.178 40.82 21.153)'),
        ('orange', 'color(--cam16-ucs 78.364 9.6945 28.629)'),
        ('yellow', 'color(--cam16-ucs 96.802 -12.779 33.037)'),
        ('green', 'color(--cam16-ucs 46.661 -26.746 20.671)'),
        ('blue', 'color(--cam16-ucs 36.252 8.5723 -37.87)'),
        ('indigo', 'color(--cam16-ucs 24.524 19.714 -22.758)'),
        ('violet', 'color(--cam16-ucs 74.738 27.949 -15.247)'),
        ('white', 'color(--cam16-ucs 100 -1.8983 -1.0754)'),
        ('gray', 'color(--cam16-ucs 56.23 -1.2555 -0.71134)'),
        ('black', 'color(--cam16-ucs 0 0 0)')
    ]

    @pytest.mark.parametrize('color1,color2', COLORS)
    def test_colors(self, color1, color2):
        """Test colors."""

        self.assertColorEqual(Color(color1).convert('cam16-ucs'), Color(color2))


class TestCAM16UCSPoperties(util.ColorAsserts, unittest.TestCase):
    """Test CAM16 UCS."""

    def test_j(self):
        """Test `j`."""

        c = Color('color(--cam16-ucs 0.51332 0.92781 1.076)')
        self.assertEqual(c['j'], 0.51332)
        c['j'] = 0.2
        self.assertEqual(c['j'], 0.2)

    def test_a(self):
        """Test `a`."""

        c = Color('color(--cam16-ucs 0.51332 0.92781 1.076)')
        self.assertEqual(c['a'], 0.92781)
        c['a'] = 0.1
        self.assertEqual(c['a'], 0.1)

    def test_b(self):
        """Test `b`."""

        c = Color('color(--cam16-ucs 0.51332 0.92781 1.076)')
        self.assertEqual(c['b'], 1.076)
        c['b'] = 0.1
        self.assertEqual(c['b'], 0.1)

    def test_alpha(self):
        """Test `alpha`."""

        c = Color('color(--cam16-ucs 0.51332 0.92781 1.076)')
        self.assertEqual(c['alpha'], 1)
        c['alpha'] = 0.5
        self.assertEqual(c['alpha'], 0.5)


class TestCAM16ApperanceModel(util.ColorAsserts, unittest.TestCase):
    """Test CAM16 appearance model."""

    CAM16 = CAM16Coords(
        45.33435136131785, 45.26195932727762, 258.92464993097565,
        62.67686398624793, 83.29355481993107, 32.720950777696196, 310.5279473979526
    )

    def test_no_lightness(self):
        """Test conversion failure when no equivalent lightness."""

        with self.assertRaises(ValueError):
            cam16_to_xyz_d65(C=self.CAM16.C, h=self.CAM16.h, env=CAM16UCS.ENV)

    def test_no_chroma(self):
        """Test conversion failure when no equivalent chroma."""

        with self.assertRaises(ValueError):
            cam16_to_xyz_d65(J=self.CAM16.J, h=self.CAM16.h, env=CAM16UCS.ENV)

    def test_no_hue(self):
        """Test conversion failure when no equivalent hue."""

        with self.assertRaises(ValueError):
            cam16_to_xyz_d65(J=self.CAM16.J, C=self.CAM16.C, env=CAM16UCS.ENV)

    def test_no_environment(self):
        """Test no test no environment."""

        with self.assertRaises(ValueError):
            cam16_to_xyz_d65(J=self.CAM16.J, C=self.CAM16.C, h=self.CAM16.h)

    def test_lightness_convert(self):
        """Test convert lightness."""

        for a, b in zip(
            cam16_to_xyz_d65(J=self.CAM16.J, C=self.CAM16.C, h=self.CAM16.h, env=CAM16UCS.ENV),
            cam16_to_xyz_d65(Q=self.CAM16.Q, C=self.CAM16.C, h=self.CAM16.h, env=CAM16UCS.ENV)
        ):
            self.assertCompare(a, b, 14)

    def test_chroma_convert(self):
        """Test convert chroma."""

        for a, b in zip(
            cam16_to_xyz_d65(J=self.CAM16.J, C=self.CAM16.C, h=self.CAM16.h, env=CAM16UCS.ENV),
            cam16_to_xyz_d65(Q=self.CAM16.Q, s=self.CAM16.s, h=self.CAM16.h, env=CAM16UCS.ENV)
        ):
            self.assertCompare(a, b, 14)

        for a, b in zip(
            cam16_to_xyz_d65(J=self.CAM16.J, C=self.CAM16.C, h=self.CAM16.h, env=CAM16UCS.ENV),
            cam16_to_xyz_d65(Q=self.CAM16.Q, M=self.CAM16.M, h=self.CAM16.h, env=CAM16UCS.ENV)
        ):
            self.assertCompare(a, b, 14)

    def test_hue_convert(self):
        """Test convert hue."""

        for a, b in zip(
            cam16_to_xyz_d65(J=self.CAM16.J, C=self.CAM16.C, h=self.CAM16.h, env=CAM16UCS.ENV),
            cam16_to_xyz_d65(J=self.CAM16.J, C=self.CAM16.C, H=self.CAM16.H, env=CAM16UCS.ENV)
        ):
            self.assertCompare(a, b, 14)

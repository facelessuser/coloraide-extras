"""Test gamut mapping."""
import unittest
from . import util
from coloraide_extras.everything import ColorAll as Color
import math


class TestHCTGamut(util.ColorAsserts, unittest.TestCase):
    """Test HCT gamut mapping by producing tonal maps."""

    def test_blue(self):
        """Test blue tonal maps."""

        hct = Color('#0000ff').convert('hct')
        tones = [100, 95, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0]
        expect = ['#ffffff', '#f1efff', '#e0e0ff', '#bec2ff',
                  '#9da3ff', '#7c84ff', '#5a64ff', '#343dff',
                  '#0000ef', '#0001ac', '#00006e', '#000000']

        # A channel should be off no more than by 1 in a scale of 0 - 255
        # Due to the fact that Material uses less precise matrices
        for tone, answer in zip(tones, expect):
            s1 = [c * 255 for c in hct.set('tone', tone).convert('srgb').fit(method='hct-chroma')[:-1]]
            s2 = [c * 255 for c in Color(answer)[:-1]]
            for c1, c2 in zip(s1, s2):
                self.assertTrue(math.isclose(c1, c2, rel_tol=1))

        hct.set('chroma', lambda c: c / 3)
        expect = ['#ffffff', '#f1efff', '#e1e0f9', '#c5c4dd',
                  '#a9a9c1', '#8f8fa6', '#75758b', '#5c5d72',
                  '#444559', '#2e2f42', '#191a2c', '#000000']

        for tone, answer in zip(tones, expect):
            s1 = [c * 255 for c in hct.set('tone', tone).convert('srgb').fit(method='hct-chroma')[:-1]]
            s2 = [c * 255 for c in Color(answer)[:-1]]
            for c1, c2 in zip(s1, s2):
                self.assertTrue(math.isclose(c1, c2, rel_tol=1))

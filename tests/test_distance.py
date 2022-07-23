"""Test distance methods."""
from coloraide_extras.everything import ColorAll as Color
from . import util
import pytest


class TestDistance(util.ColorAssertsPyTest):
    """Test distance."""

    @pytest.mark.parametrize(
        'color1,color2,value',
        [
            ('red', 'red', 0),
            ('red', 'orange', 37.32),
            ('red', 'yellow', 66.5558),
            ('red', 'green', 68.7175),
            ('red', 'blue', 71.0578),
            ('red', 'indigo', 59.7878),
            ('red', 'violet', 41.6256),
            ('red', 'white', 63.1299),
            ('red', 'black', 74.938),
            ('red', 'gray', 47.5086),
            ('red', 'red', 0),
            ('orange', 'red', 37.32),
            ('yellow', 'red', 66.5558),
            ('green', 'red', 68.7175),
            ('blue', 'red', 71.0578),
            ('indigo', 'red', 59.7878),
            ('violet', 'red', 41.6256),
            ('white', 'red', 63.1299),
            ('black', 'red', 74.938),
            ('gray', 'red', 47.5086)
        ]
    )
    def test_delta_e_cam16(self, color1, color2, value):
        """Test delta e CAM16 UCS."""

        print('color1: ', color1)
        print('color2: ', color2)
        self.assertCompare(
            Color(color1).delta_e(color2, method="cam16"),
            value,
            rounding=4
        )

    @pytest.mark.parametrize(
        'color1,color2,value',
        [
            ('red', 'red', 0),
            ('red', 'orange', 53.9171),
            ('red', 'yellow', 92.4214),
            ('red', 'green', 97.1066),
            ('red', 'blue', 101.0159),
            ('red', 'indigo', 82.9438),
            ('red', 'violet', 59.6913),
            ('red', 'white', 87.6459),
            ('red', 'black', 102.335),
            ('red', 'gray', 69.1376),
            ('red', 'red', 0),
            ('orange', 'red', 53.9171),
            ('yellow', 'red', 92.4214),
            ('green', 'red', 97.1066),
            ('blue', 'red', 101.0159),
            ('indigo', 'red', 82.9438),
            ('violet', 'red', 59.6913),
            ('white', 'red', 87.6459),
            ('black', 'red', 102.335),
            ('gray', 'red', 69.1376)
        ]
    )
    def test_delta_e_cam16_lcd(self, color1, color2, value):
        """Test delta e CAM16 LCD."""

        print('color1: ', color1)
        print('color2: ', color2)
        self.assertCompare(
            Color(color1).delta_e(color2, method="cam16", magnitude='lcd'),
            value,
            rounding=4
        )

    @pytest.mark.parametrize(
        'color1,color2,value',
        [
            ('red', 'red', 0),
            ('red', 'orange', 30.4827),
            ('red', 'yellow', 54.8533),
            ('red', 'green', 57.3138),
            ('red', 'blue', 58.8291),
            ('red', 'indigo', 49.2931),
            ('red', 'violet', 34.3513),
            ('red', 'white', 51.7972),
            ('red', 'black', 60.9053),
            ('red', 'gray', 39.3403),
            ('red', 'red', 0),
            ('orange', 'red', 30.4827),
            ('yellow', 'red', 54.8533),
            ('green', 'red', 57.3138),
            ('blue', 'red', 58.8291),
            ('indigo', 'red', 49.2931),
            ('violet', 'red', 34.3513),
            ('white', 'red', 51.7972),
            ('black', 'red', 60.9053),
            ('gray', 'red', 39.3403)
        ]
    )
    def test_delta_e_cam16_scd(self, color1, color2, value):
        """Test delta e CAM16 SCD."""

        print('color1: ', color1)
        print('color2: ', color2)
        self.assertCompare(
            Color(color1).delta_e(color2, method="cam16", magnitude='scd'),
            value,
            rounding=4
        )

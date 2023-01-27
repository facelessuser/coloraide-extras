"""HCT gamut mapping."""
from __future__ import annotations
from coloraide.gamut import Fit, clip_channels
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # pragma: no cover
    from coloraide.color import Color


class HCTChroma(Fit):
    """HCT chroma gamut mapping class."""

    NAME = "hct-chroma"

    EPSILON = 0.01
    LIMIT = 0.2
    DE = "cam16"
    DE_OPTIONS = {"magnitude": 'scd'}
    SPACE = "hct"
    MIN_LIGHTNESS = 0
    MAX_LIGHTNESS = 100
    MIN_CONVERGENCE = 0.0001

    def fit(self, color: Color, **kwargs: Any) -> None:
        """Gamut mapping via CIELCh chroma."""

        # If within gamut, just normalize hues by calling clip
        if color.in_gamut(tolerance=0):
            clip_channels(color)
            return

        space = color.space()
        mapcolor = color.convert(self.SPACE)
        lightness = mapcolor['lightness']

        # Return white or black if lightness is out of dynamic range for lightness.
        if lightness >= self.MAX_LIGHTNESS:
            clip_channels(color.update('srgb', [1.0, 1.0, 1.0], mapcolor[-1]))
            return
        elif lightness <= self.MIN_LIGHTNESS:  # pragma: no cover
            # We may never actually hit this due to the way black is cleaned up by HCT,
            # but we'll leave this in just in case something changes and we need this check.
            clip_channels(color.update('srgb', [0.0, 0.0, 0.0], mapcolor[-1]))
            return

        # Set initial chroma boundaries
        low = 0.0
        high = mapcolor['chroma']
        clip_channels(color.update(mapcolor))

        # Adjust chroma if we are not under the JND yet.
        if mapcolor.delta_e(color, method=self.DE, **self.DE_OPTIONS) >= self.LIMIT:
            # Perform "in gamut" checks until we know our lower bound is no longer in gamut.
            lower_in_gamut = True

            # If high and low get too close to converging,
            # we need to quit in order to prevent infinite looping.
            while (high - low) > self.MIN_CONVERGENCE:
                mapcolor['chroma'] = (high + low) * 0.5

                # Avoid doing expensive delta E checks if in gamut
                if lower_in_gamut and mapcolor.in_gamut(space, tolerance=0):
                    low = mapcolor['chroma']
                else:
                    clip_channels(color.update(mapcolor))
                    de = mapcolor.delta_e(color, method=self.DE, **self.DE_OPTIONS)
                    if de < self.LIMIT:
                        # Kick out as soon as we are close enough to the JND.
                        # Too far below and we may reduce chroma too aggressively.
                        if (self.LIMIT - de) < self.EPSILON:
                            break

                        # Our lower bound is now out of gamut, so all future searches are
                        # guaranteed to be out of gamut. Now we just want to focus on tuning
                        # chroma to get as close to the JND as possible.
                        if lower_in_gamut:
                            lower_in_gamut = False
                        low = mapcolor['chroma']
                    else:
                        # We are still outside the gamut and outside the JND
                        high = mapcolor['chroma']

"""Delta E CAM16."""
from __future__ import annotations
import math
from coloraide.distance import DeltaE
from coloraide import algebra as alg
from typing import Any, TYPE_CHECKING, cast

if TYPE_CHECKING:  # pragma: no cover
    from coloraide import Color
    from ..spaces.hct import HCT


class DEHCT(DeltaE):
    """Delta E HCT class."""

    NAME = "hct"

    @classmethod
    def distance(cls, color: Color, sample: Color, **kwargs: Any) -> float:
        """Delta E z color distance formula."""

        hct = cast("HCT", color.CS_MAP['hct'])
        h1, c1, t1 = alg.no_nans(color.convert('hct')[:-1])
        h2, c2, t2 = alg.no_nans(sample.convert('hct')[:-1])

        # Convert HCT C (CAM16 M) to CAM16 UCS a and b components, the same as DE CAM16.
        hrad = math.radians(h1)
        m = math.log(1 + hct.ENV.c2 * c1) / hct.ENV.c2
        a1 = m * math.cos(hrad)
        b1 = m * math.sin(hrad)

        hrad = math.radians(h2)
        m = math.log(1 + hct.ENV.c2 * c2) / hct.ENV.c2
        a2 = m * math.cos(hrad)
        b2 = m * math.sin(hrad)

        # Lightness adjustments from DE 2000
        lpm = (t1 + t2) / 2
        l_temp = (lpm - 50) ** 2
        sl = 1 + ((0.015 * l_temp) / math.sqrt(20 + l_temp))

        return math.sqrt(((t1 - t2) / sl) ** 2 + (a1 - a2) ** 2 + (b1 - b2) ** 2)

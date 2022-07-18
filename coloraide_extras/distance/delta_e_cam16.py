"""Delta E CAM16."""
import math
from coloraide.distance import DeltaE
from coloraide import algebra as alg
from typing import Any, cast, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from coloraide import Color
    from ..spaces.cam16_ucs import CAM16UCS


class DECAM16(DeltaE):
    """Delta E z class."""

    NAME = "cam16"

    @classmethod
    def distance(cls, color: 'Color', sample: 'Color', magnitude: str = 'ucs', **kwargs: Any) -> float:
        """Delta E z color distance formula."""

        space = 'cam16-{}'.format(magnitude)
        cam16 = color.CS_MAP[space]
        j1, a1, b1 = alg.no_nans(color.convert(space)[:-1])
        j2, a2, b2 = alg.no_nans(sample.convert(space)[:-1])

        dj = j1 - j2
        da = a1 - a2
        db = b1 - b2
        kl = cast('CAM16UCS', cam16).ENV.kl

        return math.sqrt((dj / kl) ** 2 + da ** 2 + db ** 2)

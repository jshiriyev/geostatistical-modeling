from dataclasses import dataclass

import numpy

@dataclass
class Slot:
    """It is a well item dictionary."""
    name 		: str

    index 		: int = None
    field 		: str = None
    platform 	: str = None

    xhead 		: float = 0.0
    yhead 		: float = 0.0
    datum 		: float = 0.0

    status 		: str = "prospect"
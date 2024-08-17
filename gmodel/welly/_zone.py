from dataclasses import dataclass

import numpy

@dataclass
class Zone:
    """It is a formation zone dictionary."""

    name    : str
    field   : str = None
    color   : str = "white"
    hatch   : str = ".."
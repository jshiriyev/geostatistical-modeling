from dataclasses import dataclass

@dataclass
class Zone:
    """It is a formation zone dictionary."""

    name    : str = None
    field   : str = None
    color   : str = "white"
    hatch   : str = ".."
from dataclasses import dataclass

@dataclass
class Zone:
    """It is a formation zone dictionary."""

    name    : str = None
    depth   : float = None
    color   : str = "white"
    hatch   : str = ".."
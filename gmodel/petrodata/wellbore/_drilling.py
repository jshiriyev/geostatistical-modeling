from dataclasses import dataclass

import datetime

@dataclass
class Drilling:
	"""It is a drilling dictionary for a well."""
	start	: datetime.date = None
	end		: datetime.date = None

@dataclass
class Target:
	"""It is a Target dictionary for a well."""
	x 		: float = None
	y 		: float = None

@dataclass
class Slot:
    """It is a slot dictionary for a well."""
    index 	: int = None

    plt 	: str = None

    xhead 	: float = 0.0
    yhead 	: float = 0.0
    datum 	: float = 0.0

@dataclass
class Casing:
	"""It is a slot dictionary for a well."""
	shoe 	: float = None
	diam 	: float = None

if __name__ == "__main__":

	drill = Drilling(
		datetime.date(1990,2,2),
		datetime.date(1990,4,3),
		)

	print(drill.end)
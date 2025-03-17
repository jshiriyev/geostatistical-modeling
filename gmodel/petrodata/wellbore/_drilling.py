from dataclasses import dataclass

from datetime import date

@dataclass
class Target:
	"""It is a Target dictionary for a well."""
	x 		: float = None
	y 		: float = None

@dataclass
class Drilling:
	"""It is a drilling dictionary for a well."""
	start	: date = None
	end		: date = None

	depth 	: float = None

	## add target

if __name__ == "__main__":

	drill = Drilling(
		date(1990,2,2),
		date(1990,4,3),
		)

	print(drill.end)
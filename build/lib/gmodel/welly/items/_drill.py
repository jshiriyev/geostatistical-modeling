from dataclasses import dataclass

import datetime

@dataclass
class Drill:
	"""It is a drilling dictionary for a well"""

	start		: datetime.date = None
	end			: datetime.date = None

	layer		: str = None
	depth		: float = None

if __name__ == "__main__":

	drill = Drill(
		datetime.date(1990,2,2),
		datetime.date(1990,4,3),
		layer="SP",
		depth=3500,
		)

	print(drill.end)
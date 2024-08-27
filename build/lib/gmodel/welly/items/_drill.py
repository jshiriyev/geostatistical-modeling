from dataclasses import dataclass

import datetime

@dataclass
class Drill:
	"""It is a drilling dictionary for a well"""

	start		: datetime.date = None
	end			: datetime.date = None

	layer		: str = None
	depth		: float = None

	target		: dict = None

	def __post_init__(self):

		self.target = Target(**(self.target or {}))

@dataclass
class Target:
	"""It is a Target dictionary for a Drill"""

	layer 		 : str = None
	depth 		 : float = None

if __name__ == "__main__":

	drill = Drill(
		datetime.date(1990,2,2),
		datetime.date(1990,4,3),
		layer="SP",
		depth=3500,
		target = dict(layer="KaS",depth=3700)
		)

	print(drill.end)
from dataclasses import dataclass

from ._survey import Depth

@dataclass
class Casing:
	"""It is a casing dictionary for a well."""
	ID  	: float = None # Inner diameter

	depth 	: dict = None # MD of casing shoe
	top  	: dict = None # MD of casing top

	def __post_init__(self):

		self.depth = Depth(**(self.depth or {}))
		self.top = Depth(**(self.top or {}))

@dataclass
class Tubing:
	"""It is a casing dictionary for a well."""
	ID 		: float = None # Inner diameter
	OD		: float = None # Outer diameter

	depth 	: dict = None # MD of tubing

	def __post_init__(self):

		self.depth = Depth(**(self.depth or {}))

class Layout():

	def __init__(self,casings:list=None,tubings:list=None):

		self.casings = [] if casings is None else casings
		self.tunings = [] if tubings is None else tubings


from dataclasses import dataclass

@dataclass
class Casing:
	"""It is a casing dictionary for a well."""
	depth 	: float = None # MD of casing shoe
	ID  	: float = None # Inner diameter

@dataclass
class Tubing:
	"""It is a casing dictionary for a well."""
	depth 	: float = None # MD of tubing
	ID 		: float = None # Inner diameter
	OD		: float = None # Outer diameter

class Layout():

	def __init__(self,casings:list=None,tubings:list=None):

		self.casings = [] if casings is None else casings
		self.tunings = [] if tubings is None else tubings


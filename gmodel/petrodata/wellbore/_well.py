from dataclasses import dataclass

import numpy

from .items._drilling import Drilling

from .items._layout import Layout
from .items._survey import Survey

from .items._zones import Zones
from .items._perfs import Perf

@dataclass
class Name:

    name : str

    @staticmethod
    def get(index:int,template:str) -> str:
        """Generates a well name by formatting a given index into a string template.

        Parameters:
            index    : The well index (number)
            template : A string template containing a placeholder (e.g., "Well-{}").
        
        Returns:
            str: The formatted well name.

        Raises:
            ValueError: If the template does not contain a valid placeholder.
        """
        try:
            return template.format(index)
        except Error as e:
            raise ValueError(f"Invalid template '{template}' for index '{index}'. Error: {e}")

    @staticmethod
    def digits(name:str) -> str:
        """Returns digits or characters enclosed in single quotes from a given string.
        If no match is found, returns the original string.

        Parameters:
        - name (str): The input string.

        Returns:
        - str: The extracted content inside single quotes, or the original string if no match is found.
        """
        match = re.search(r"'([^']*)'",name) # chatgpt suggested
        # match = re.search(r"'(.*?)'",name) # previous version

        return match.group(1) if match else name

@dataclass
class Slot:
    """It is a slot dictionary for a well."""
    index   : int = None

    plt     : str = None

    xhead   : float = 0.0
    yhead   : float = 0.0
    datum   : float = 0.0

class Well():
    """It is a well dictionary with all sub classes."""

    def __init__(self,
        name        : str,
        status      : str = "active",
        slot        : dict = None,
        drilling    : dict = None,
        layout      : dict = None,
        survey      : dict = None,
        zones       : dict = None,
        perfs       : dict = None,
        ):

        self.name   = name
        self.status = status

        self.slot   = slot
        self.drilling  = drilling
        self.layout = layout
        self.survey = survey
        self.zones  = zone
        self.perfs  = perfs

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,value:dict):
        self._name = str(value)

    @property
    def field(self):
        return self._field

    @field.setter
    def field(self,value:dict):
        self._field = str(value)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self,value:dict):
        self._status = str(value)

    @property
    def slot(self):
        return self._slot

    @slot.setter
    def slot(self,value:dict):
        self._slot = Slot(**(value or {}))

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self,value:dict):
        self._target = Target(**(value or {}))

    @property
    def drill(self):
        return self._drill

    @drill.setter
    def drill(self,value:dict):
        self._drill = Drill(**(value or {}))

    @property
    def layout(self):
        return self._layout

    @layout.setter
    def layout(self,value:dict):
        self._layout = Layout(**(value or {}))

    @property
    def survey(self):
        return self._survey

    @survey.setter
    def survey(self,value:dict):
        self._survey = Survey(**(value or {}))

    @property
    def zone(self):
        return self._zone

    @zone.setter
    def zone(self,value:dict):
        self._zone = Zone(**(value or {}))

    @property
    def perfs(self):
        return self._perfs

    @perfs.setter
    def perfs(self,value:dict):
        self._perfs = Perfs(**(value or {}))
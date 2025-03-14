import numpy

from .items._slot import Slot

from .items._target import Target

from .items._drill import Drill

from .items._layout import Layout
from .items._survey import Survey

from .items._zone import Zone

from .items._perfs import Perfs

class Well():
    """It is a well dictionary with all sub classes."""

    def __init__(self,name:str=None,field:str=None,status:str="active",
        slot:dict=None,target:dict=None,drill:dict=None,layout:dict=None,survey:dict=None,zone:dict=None,perfs:dict=None):

        self.name   = name
        self.field  = field
        self.status = status

        self.slot   = slot
        self.target = target
        self.drill  = drill
        self.layout = layout
        self.survey = survey
        self.zone   = zone
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
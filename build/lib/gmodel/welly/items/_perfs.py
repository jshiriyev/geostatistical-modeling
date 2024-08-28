from dataclasses import dataclass, fields

import datetime

import pandas

@dataclass
class PerfData:
    """It is a perforation dictionary for a perf in a well."""

    date        : datetime.date = None

    layer       : str = None
    interval    : str = None
    guntype     : str = None

    @staticmethod
    def fields() -> list:
        return [field.name for field in fields(PerfData)]

class Perfs():

    def __init__(self,frame:pandas.DataFrame=None,mapping:dict=None):
        """
        Initialize the class with a DataFrame and a column mapping.

        Parameters:

        frame (pd.DataFrame)    : The input DataFrame.

        mapping (dict)          : A dictionary mapping class properties
                                to DataFrame columns.
        """
        self.frame,self.mapping = frame,mapping

        self.validate_mapping()

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self,value:pandas.DataFrame):
        self._frame = pandas.DataFrame(columns=PerfData.fields()) if value is None else value

    @property
    def mapping(self):
        return self._mapping

    @mapping.setter
    def mapping(self,value:dict):
        self._mapping = {key:key for key in PerfData.fields()} if value is None else value

    def validate_mapping(self):

        wrong_keys = [key for key in self.mapping.keys() if key not in PerfData.fields()]

        if wrong_keys:
            raise ValueError(f"There are wrong keys in the mapping: {', '.join(wrong_keys)}")

    def __getattr__(self,key):

        if key in PerfData.fields():
            return self.frame[self.mapping[key]].unique()

        return getattr(self.frame,key)

    def __getitem__(self,key):

        if isinstance(key,int):

            row = self.frame.iloc[key].to_dict()

            return PerfData(**{key:row.get(value) for key,value in self.mapping.items()})

        return getitem(self.frame,key)

    @staticmethod
    def interval_string_to_list(value:str,delimiter="-",decsep="."):

        depths = value.split(delimiter)

        depths = [float(depth.replace(decsep,'.')) for depth in depths]

        if len(depths)==1:
            depths.append(None)

        return depths
    
if __name__ == "__main__":

    frame = pandas.DataFrame(dict(
        A=[datetime.date(2020,1,1),datetime.date(2021,1,1),datetime.date(2022,1,1),datetime.date(2023,1,1)],
        B=['A','B','C','D'],
        C=['5-6','7-8','9-10','11'],
        D=['XY','XZ','YZ','ZZ']))

    perfs = Perfs(frame,dict(date='A',layer='B',interval='C',guntype='D'))

    # help(frame.__getitem__)

    print(perfs.mapping)
    print(perfs[2].date)

    print(perfs.layer)

    perfs2 = Perfs()

    print(perfs2.mapping)

    # for d in dir(frame):
    #     print(d)

    
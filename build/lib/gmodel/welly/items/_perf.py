from dataclasses import dataclass

import datetime

@dataclass
class Perf:
    """It is a perforation dictionary for a perf in a well."""

    date        : datetime.date = None

    layer       : str = None
    interval    : str = None
    guntype     : str = None

    @staticmethod
    def interval_string_to_list(value:str,delimiter="-",decsep="."):

        depths = value.split(delimiter)

        depths = [float(depth.replace(decsep,'.')) for depth in depths]

        if len(depths)==1:
            depths.append(None)

        return depths
from dataclasses import dataclass, fields

@dataclass
class Operation:
    """It is a Production  dictionary for a perf in a well."""

    date    : datetime.date = None

    well    : str = None

    horizon : str = None

    days    : int = None

    optype  : str = "production"

    orate   : float = None
    wrate   : float = None
    grate   : float = None

    @staticmethod
    def fields() -> list:
        return [field.name for field in fields(Operation)]
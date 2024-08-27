from dataclasses import dataclass

import numpy

@dataclass
class Survey:
    """It is a well survey (direction or trajectory)."""

    MD      : numpy.ndarray = None
    TVD     : numpy.ndarray = None
    DX      : numpy.ndarray = None
    DY      : numpy.ndarray = None
    INC     : numpy.ndarray = None
    AZI     : numpy.ndarray = None

    @staticmethod
    def inc2tvd(MD:numpy.ndarray,INC:numpy.ndarray):

        TVD = MD.copy()

        offset = MD[1:]-MD[:-1]
        radian = INC[1:]/180*numpy.pi

        TVD[1:] = numpy.cumsum(offset*numpy.cos(radian))

        return TVD

    @staticmethod
    def off2tvd(MD:numpy.ndarray,DX:numpy.ndarray,DY:numpy.ndarray):

        TVD = MD.copy()

        offMD = MD[1:]-MD[:-1]
        offDX = DX[1:]-DX[:-1]
        offDY = DY[1:]-DY[:-1]
                         
        TVD[1:] = numpy.sqrt(offMD**2-offDX**2-offDY**2)

        return numpy.cumsum(TVD)
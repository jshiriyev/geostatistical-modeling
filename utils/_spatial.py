import numpy

class Spatial(numpy.ndarray):

    """It is a numpy array of shape (N,) with additional spatial attributes x,y,z"""

    def __new__(cls,vals,xaxis=None,yaxis=None,zaxis=None):
        """it is a subclass of numpy.ndarray where x,y,z coordinates can be defined"""

        obj = numpy.asarray(vals).view(cls)

        if xaxis is None:
            obj.xaxis = numpy.arange(obj.size)
        else:
            obj.xaxis = numpy.asarray(xaxis).flatten()

        obj.yaxis = yaxis if yaxis is None else numpy.asarray(yaxis).flatten()
        obj.zaxis = zaxis if zaxis is None else numpy.asarray(zaxis).flatten()

        return obj

    def __array_finalize__(self,obj):

        if obj is None: return

        self.xaxis = getattr(obj,'xaxis',None)
        self.yaxis = getattr(obj,'yaxis',None)
        self.zaxis = getattr(obj,'zaxis',None)

    @property
    def coord(self):
        return numpy.array([self.xaxis,self.yaxis,self.zaxis]).T

    def get_delta(self,v=None):
        v = self if v is None else v
        return self-v.reshape((-1,1))

    @property
    def delta(self):
        return self.get_delta()
    
    def get_xdelta(self,v=None):
        v_xaxis = self.xaxis if v is None else v.xaxis
        return self.xaxis-v_xaxis.reshape((-1,1))

    def get_ydelta(self,v=None):
        v_yaxis = self.yaxis if v is None else v.yaxis
        return self.yaxis-v_yaxis.reshape((-1,1))

    def get_zdelta(self,v=None):
        v_zaxis = self.zaxis if v is None else v.zaxis
        return self.zaxis-v_zaxis.reshape((-1,1))

    @property
    def xdelta(self):
        return self.get_xdelta()

    @property
    def ydelta(self):
        return self.get_ydelta()

    @property
    def zdelta(self):
        return self.get_zdelta()

    def get_distmat(self,v=None):

        xdelta = self.get_xdelta(v)
        
        ydelta = 0 if self.yaxis is None else self.get_ydelta(v)
        zdelta = 0 if self.zaxis is None else self.get_zdelta(v)

        return numpy.sqrt(xdelta**2+ydelta**2+zdelta**2)
    
    @property
    def distmat(self):
        return self.get_distmat()

    @property
    def azimmat(self):
        return numpy.arctan2(self.ydelta,self.xdelta)

if __name__ == "__main__":

    u = Spatial([5,6,7,8],[0,1,2,3],[0,1,2,3])

    # print(u)
    # print(u.xdelta)
    # print(u.xaxis)
    print(u.distmat)
    # print(u.azimmat)


import numpy

from scipy.stats import norm

class variogram(numpy.ndarray):

    """It is a numpy array of shape (N,) with additional spatial attributes x,y,z"""

    def __new__(cls,vals,x=None,y=None,z=None):
        """it is a subclass of numpy.ndarray where x,y,z coordinates can be defined"""

        obj = numpy.asarray(vals).view(cls)

        obj.x = x if x is None else numpy.asarray(x).flatten()
        obj.y = y if y is None else numpy.asarray(y).flatten()
        obj.z = z if z is None else numpy.asarray(z).flatten()

        return obj

    def __array_finalize__(self,obj):

        if obj is None: return

        self.x = getattr(obj,'x',None)
        self.y = getattr(obj,'y',None)
        self.z = getattr(obj,'z',None)

    @property
    def dx(self):
        return 0 if self.x is None else self.get_delta(self.x,self.x)

    @property
    def dy(self):
        return 0 if self.y is None else self.get_delta(self.y,self.y)

    @property
    def dz(self):
        return 0 if self.z is None else self.get_delta(self.z,self.z)
    
    @property
    def distmat(self):
        return numpy.sqrt(self.dx**2+self.dy**2+self.dz**2)

    @property
    def azimmat(self):
        return numpy.arctan2(self.dy,self.dx)

    @property
    def isolag(self):
        return self.distmat[self.distmat!=0].min()

    @staticmethod
    def get_expbins(lag,lagtol,lagmax):
        return numpy.arange(lag,lagmax+lagtol/2,lag)

    def set_experimental(self,lag=None,lagtol=None,lagmax=None,azimuth=None,azimuthtol=None,bandwidth=None,returnFlag=False):
        """
        Azimuth range is (-\\pi,\\pi] in radians and (-180,180] in degrees.
        If we set +x to east and +y to north then the azimuth is selected
        to be zero in the +x direction and positive counterclockwise.
        """
        
        prop_err = self.get_delta(self,self)**2

        """for an anisotropy only 2D data can be used FOR NOW"""

        self.azimuth = 0 if azimuth is None else numpy.radians(azimuth)
        self.azimuthtol = numpy.pi if azimuth is None else numpy.radians(azimuthtol)
        self.bandwidth = numpy.inf if azimuth is None else bandwidth

        delta_angle = numpy.abs(self.angle-self.azimuth)
        
        con_azmtol = delta_angle<=self.azimuthtol
        con_banwdt = numpy.sin(delta_angle)*self.distance<=(self.bandwidth/2.)
        con_direct = numpy.logical_and(con_azmtol,con_banwdt)

        con_ = numpy.logical_and(self.distance!=0,con_azmtol)

        self.lag = self.distance[con_].min() if lag is None else lag

        self.lagtol = self.lag/2. if lagtol is None else lagtol
        self.lagmax = self.distance[con_azmtol].max() if lagmax is None else lagmax

        self.outbound = self.lagmax+self.lagtol

        """bins is the array of lag distances"""

        self.experimental = numpy.zeros_like(self.bins_experimental)
        
        for i,h in enumerate(self.bins_experimental):

            con_distnc = numpy.abs(self.distance-h)<=self.lagtol

            conoverall = numpy.logical_and(con_distnc,con_direct)

            num_matchcon = numpy.count_nonzero(conoverall)

            if num_matchcon==0:
                self.experimental[i] = numpy.nan
            else:
                semivariance = prop_err[conoverall].sum()/(2*num_matchcon)
                self.experimental[i] = semivariance

        if returnFlag:
            return self.bins_experimental,self.experimental

    def set_searchbox(self,origin_x=0,origin_y=0):
        """Nomenclature-BEGINNING"""
        ## alpha  : azimuth_tol at bandwidth dominated section
        ## omega  : bandwidth at azimuth_tol dominated section
        ## theta  : azimuth range at the specified distance
        """Nomenclature-END"""

        def azmtol(bandwidth,bound,azm_tol):
            return(numpy.arcsin(min(numpy.sin(azm_tol),bandwidth/bound)))

        def bndwdt(bandwidth,bound,azm_tol):
            return min(bandwidth,bound*numpy.sin(azm_tol))

        alpha = azmtol(self.bandwidth,self.outbound,self.azimuthtol)
        omega = bndwdt(self.bandwidth,self.outbound,self.azimuthtol)

        theta = numpy.linspace(self.azimuth-alpha,self.azimuth+alpha)
        sides = omega/numpy.sin(self.azimuthtol)

        xO1 = self.outbound*numpy.cos(self.azimuth)
        yO1 = self.outbound*numpy.sin(self.azimuth)

        xO2 = self.outbound*numpy.cos(self.azimuth-alpha)
        yO2 = self.outbound*numpy.sin(self.azimuth-alpha)

        xO3 = self.outbound*numpy.cos(self.azimuth+alpha)
        yO3 = self.outbound*numpy.sin(self.azimuth+alpha)

        xO4 = sides*numpy.cos(self.azimuth-self.azimuthtol)
        yO4 = sides*numpy.sin(self.azimuth-self.azimuthtol)

        xO5 = sides*numpy.cos(self.azimuth+self.azimuthtol)
        yO5 = sides*numpy.sin(self.azimuth+self.azimuthtol)

        x1 = numpy.linspace(0,xO1)
        y1 = numpy.linspace(0,yO1)

        x2 = numpy.linspace(xO4,xO2)
        y2 = numpy.linspace(yO4,yO2)

        x3 = numpy.linspace(xO5,xO3)
        y3 = numpy.linspace(yO5,yO3)

        x4 = numpy.linspace(0,xO4)
        y4 = numpy.linspace(0,yO4)

        x5 = numpy.linspace(0,xO5)
        y5 = numpy.linspace(0,yO5)

        x6 = self.outbound*numpy.cos(theta)
        y6 = self.outbound*numpy.sin(theta)

        plt.plot(origin_x+x1,origin_y+y1,'b--')
        plt.plot(origin_x+x2,origin_y+y2,'k')
        plt.plot(origin_x+x3,origin_y+y3,'k')
        plt.plot(origin_x+x4,origin_y+y4,'k')
        plt.plot(origin_x+x5,origin_y+y5,'k')
        plt.plot(origin_x+x6,origin_y+y6,'k')

        for h in self.bins_experimental:
            
            hmin = h-self.lagtol
            
            hmin_alpha = azmtol(self.bandwidth,hmin,self.azimuthtol)
            hmin_theta = numpy.linspace(self.azimuth-hmin_alpha,self.azimuth+hmin_alpha)
            
            hmin_x = hmin*numpy.cos(hmin_theta)
            hmin_y = hmin*numpy.sin(hmin_theta)

            plt.plot(origin_x+hmin_x,origin_y+hmin_y,'r')

    def set_theoretical(self,vbins=None,vtype='spherical',vsill=None,vrange=None,vnugget=0,**kwars):

        if vbins is None:
            if hasattr(self,"bins_experimental"):
                d = self.bins_experimental
            elif hasattr(self,"distance"):
                d = self.distance
        else:
            self.bins_theoretical = vbins
            d = vbins
        
        self.type = vtype

        if vsill is None:
            self.sill = self.var().tolist()
        else:
            self.sill = vsill
        
        if vrange is None:
            self.range = (d.max()-d.min())/5
        else:
            self.range = vrange

        self.nugget = vnugget

        self.theoretical,self.covariance = self.get_varmodel(
            d,self.type,self.sill,self.range,self.nugget,**kwars)

    @staticmethod
    def get_dist(A,B):

        dist = numpy.zeros((A.shape[0],A.shape[0]))

        for a,b in zip(A.T,B.T):
            dist += (a-b.reshape((-1,1)))**2

        return numpy.sqrt(dist)

    @staticmethod
    def get_delta(A,B):
        return A-B.reshape((-1,1))

    @staticmethod
    def get_varmodel(model,*args,**kwargs):
        return getattr(self,f"get_var{model}")(*args,**kwargs)

    @staticmethod
    def get_varpower(h,c,p=1,c0=0):
        gamma = numpy.zeros_like(h)
        gamma[h>0] = c0+(c-c0)*(h[h>0])**p
        return gamma

    @staticmethod
    def get_varspherical(h,c,a,c0=0):
        gamma = numpy.zeros_like(h)
        ratio = h[h>0]/a
        gamma[h>0] = c0+(c-c0)*(3/2*ratio-1/2*ratio**3)
        gamma[h>a] = c
        return gamma

    @staticmethod
    def get_varexponential(h,c,a,c0=0):
        gamma = numpy.zeros_like(h)
        ratio = h[h>0]/a
        gamma[h>0] = c0+(c-c0)*(1-numpy.exp(-3*ratio))
        return gamma

    @staticmethod
    def get_vargaussian(h,c,a,c0=0):
        gamma = numpy.zeros_like(h)
        ratio = h[h>0]/a
        gamma[h>0] = c0+(c-c0)*(1-numpy.exp(-3*ratio**2))
        return gamma

    @staticmethod
    def get_varholeeffect(h,c,a,c0=0):
        gamma = numpy.zeros_like(h)
        ratio = h[h>0]/a
        gamma[h>0] = c0+(c-c0)*(1-numpy.sin(ratio)/ratio)
        return gamma

    @staticmethod
    def get_varcubic(h,c,a,c0=0):
        gamma = numpy.zeros_like(h)
        ratio = h[h>0]/a
        gamma[h>0] = c0+(c-c0)*(7*ratio**2-35/4*ratio**3+7/2*ratio**5-3/4*ratio**7)
        gamma[h>a] = c
        return gamma

    @staticmethod
    def get_varcauchy(h,c,a,c0=0):
        gamma = numpy.zeros_like(h)
        ratio = h[h>0]/a
        gamma[h>0] = c0+(c-c0)*(1-1/(1+ratio**2))
        return gamma

    @staticmethod
    def get_vardewijs(h,c,c0=0):
        gamma = numpy.zeros_like(h)
        gamma[h>0] = c0+(c-c0)*numpy.log(h[h>0])
        return gamma

if __name__ == "__main__":

    import matplotlib.pyplot as plt
    import numpy as np

    A = variogram([1,2,3,4],x=[0.1,0.2,0.3,0.4])

    print(A.distmat)

    h = np.linspace(0,40,1000)

    c = 1
    a = 10
    c0 = 0.1

    gamma1 = A.get_varpower(h,c,p=0.2,c0=c0)
    gamma2 = A.get_varspherical(h,c,a,c0=c0)
    gamma3 = A.get_varexponential(h,c,a,c0=c0)
    gamma4 = A.get_vargaussian(h,c,a,c0=c0)
    gamma5 = A.get_varholeeffect(h,c,a,c0=c0)
    gamma6 = A.get_varcubic(h,c,a,c0=c0)
    gamma7 = A.get_varcauchy(h,c,a,c0=c0)
    gamma8 = A.get_vardewijs(h,c,c0=c0)

    plt.plot(h[1:],gamma1[1:],label="1")
    plt.plot(h[1:],gamma2[1:],label="2")
    plt.plot(h[1:],gamma3[1:],label="3")
    plt.plot(h[1:],gamma4[1:],label="4")
    plt.plot(h[1:],gamma5[1:],label="5")
    plt.plot(h[1:],gamma6[1:],label="6")
    plt.plot(h[1:],gamma7[1:],label="7")
    plt.plot(h[1:],gamma8[1:],label="8")

    plt.xlim([0,40])
    plt.ylim(ymin=0)

    plt.legend()

    plt.show()


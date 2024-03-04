from dataclasses import dataclass

from matplotlib import pyplot

import numpy

from utils._spatial import Spatial

@dataclass(frozen=True)
class Experimental:
    """It is a variogram property dictionary."""
    lagdist     : float = None
    lagtol      : float = None
    outbound    : float = None
    azimuth     : float = 0.0
    azimtol     : float = numpy.pi
    bdwidth     : float = numpy.inf

    @property
    def params(self):
        return {
            "lagdist"   : self.lagdist,
            "lagtol"    : self.lagtol,
            "outbound"  : self.outbound
            }
    
    @property
    def anisoparams(self):
        return {
            "azimuth"   : numpy.radians(self.azimuth),
            "azimtol"   : numpy.radians(self.azimtol),
            "bdwidth"   : self.bdwidth
            }

@dataclass(frozen=True)
class Theoretical:
    """It is a variogram property dictionary."""
    model       : str   = "spherical"
    sill        : float = None
    vrange      : float = None
    power       : float = None
    nugget      : float = 0.0

    @property
    def params(self):
        return {
            "sill"      : self.sill,
            "vrange"    : self.vrange,
            "power"     : self.power,
            "nugget"    : self.nugget
            }

class Variogram():

    @staticmethod
    def isolag(data:Spatial):
        return data.distmat[data.distmat!=0].min()

    @staticmethod
    def azimbool(data:Spatial,exp:Experimental):

        params = exp.anisoparams

        thetadelta = numpy.abs(data.azimmat-params["azimuth"])

        atolbool = thetadelta<=params["azimtol"]
        bandbool = numpy.sin(thetadelta)*data.distmat<=(params['bdwidth']/2.)
        
        return numpy.logical_and(atolbool,bandbool)

    @staticmethod
    def anisolag(data:Spatial,exp:Experimental):

        azimbool = Variogram.azimbool(data,exp)
        azimbool = numpy.logical_and(data.distmat!=0,azimbool)

        return data.distmat[azimbool].min()

    @staticmethod
    def outbound(data:Spatial,exp:Experimental):

        azimuth = exp.anisoparams['azimuth']

        xmax = numpy.abs(data.xdelta).max()

        ymax = 0 if data.yaxis is None else numpy.abs(data.ydelta).max()

        costheta = numpy.inf if numpy.cos(azimuth)==0 else numpy.cos(azimuth)
        sintheta = numpy.inf if numpy.sin(azimuth)==0 else numpy.sin(azimuth)

        return min(xmax/costheta,ymax/sintheta)

    @staticmethod
    def bins(exp:Experimental):

        return numpy.arange(exp.params['lagdist'],
            exp.params['outbound']+exp.params['lagdist']/2,
            exp.params['lagdist']
            )

    @staticmethod
    def experimental(data:Spatial,exp:Experimental):
        """anisoparams calculations are carried only in 2D space:

        azimuth : search direction, range is (-pi,pi] in radians
                  and (-180,180] in degrees. If we set +x to east and
                  +y to north then the azimuth is selected to be zero in the
                  +x direction and positive counterclockwise.
        """
        
        delta = data.delta**2

        abool = Variogram.azimbool(data,exp)
        hbins = Variogram.bins(exp)

        gamma = numpy.zeros_like(hbins)
        
        for i,h in enumerate(hbins):

            dbool = numpy.abs(data.distmat-h)<=exp.params['lagtol']
            cbool = numpy.logical_and(dbool,abool)

            N = numpy.count_nonzero(cbool)

            gamma[i] = numpy.nan if N==0 else delta[cbool].sum()/(2*N)

        return gamma,hbins

    @staticmethod
    def azimtol(exp:Experimental):

        params = exp.anisoparams

        theta1 = numpy.sin(params['azimtol'])
        theta2 = params['bdwidth']/exp.params['outbound']

        return numpy.arcsin(min(theta1,theta2))

    @staticmethod
    def bdwidth(exp:Experimental):

        params = exp.anisoparams

        width1 = params['bdwidth']
        width2 = exp.params['outbound']*numpy.sin(params['azimtol'])

        return min(width1,width2)

    @staticmethod
    def searchbox(exp:Experimental,xorigin=0,yorigin=0):
        """
        alpha  : azimuth_tol at bandwidth dominated section
        omega  : bandwidth at azimuth_tol dominated section
        theta  : azimuth range at the specified distance
        """

        alpha = Variogram.azimtol(exp)
        omega = Variogram.bdwidth(exp)

        params = exp.anisoparams

        theta = numpy.linspace(params['azimuth']-alpha,params['azimuth']+alpha)
        sides = omega/numpy.sin(params['azimtol'])

        xO1 = exp.outbound*numpy.cos(params['azimuth'])
        yO1 = exp.outbound*numpy.sin(params['azimuth'])

        xO2 = exp.outbound*numpy.cos(params['azimuth']-alpha)
        yO2 = exp.outbound*numpy.sin(params['azimuth']-alpha)

        xO3 = exp.outbound*numpy.cos(params['azimuth']+alpha)
        yO3 = exp.outbound*numpy.sin(params['azimuth']+alpha)

        xO4 = sides*numpy.cos(params['azimuth']-params['azimtol'])
        yO4 = sides*numpy.sin(params['azimuth']-params['azimtol'])

        xO5 = sides*numpy.cos(params['azimuth']+params['azimtol'])
        yO5 = sides*numpy.sin(params['azimuth']+params['azimtol'])

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

        x6 = exp.outbound*numpy.cos(theta)
        y6 = exp.outbound*numpy.sin(theta)

        pyplot.plot(xorigin+x1,yorigin+y1,'b--')
        pyplot.plot(xorigin+x2,yorigin+y2,'k')
        pyplot.plot(xorigin+x3,yorigin+y3,'k')
        pyplot.plot(xorigin+x4,yorigin+y4,'k')
        pyplot.plot(xorigin+x5,yorigin+y5,'k')
        pyplot.plot(xorigin+x6,yorigin+y6,'k')

        for h in Variogram.bins(**exp.params):
            
            hmin = h-exp.lagtol
            
            hmin_alpha = Variogram.azimtol(hmin,params['azimtol'],params['bdwidth'])
            hmin_theta = numpy.linspace(params['azimuth']-hmin_alpha,params['azimuth']+hmin_alpha)
            
            hmin_x = hmin*numpy.cos(hmin_theta)
            hmin_y = hmin*numpy.sin(hmin_theta)

            pyplot.plot(xorigin+hmin_x,yorigin+hmin_y,'r')

    @staticmethod
    def theoretical(bins,theory:Theoretical):

        return Variogram.get_varmodel(bins,theory)

    @staticmethod
    def get_varmodel(bins,theory:Theoretical):

        kwargs = theory.params

        try:
            model = kwargs.pop("model")
        except KeyError:
            model = 'spherical'

        return getattr(Variogram,f"get_var{model}")(bins,**kwargs)

    @staticmethod
    def get_varpower(bins,sill,power=1,nugget=0):
        gamma = numpy.zeros_like(bins)
        gamma[bins>0] = nugget+(sill-nugget)*(bins[bins>0])**power
        return gamma

    @staticmethod
    def get_varspherical(bins,sill,vrange,nugget=0):
        gamma = numpy.zeros_like(bins)
        ratio = bins[bins>0]/vrange
        gamma[bins>0] = nugget+(sill-nugget)*(3/2*ratio-1/2*ratio**3)
        gamma[bins>vrange] = sill
        return gamma

    @staticmethod
    def get_varexponential(bins,sill,vrange,nugget=0):
        gamma = numpy.zeros_like(bins)
        ratio = bins[bins>0]/vrange
        gamma[bins>0] = nugget+(sill-nugget)*(1-numpy.exp(-3*ratio))
        return gamma

    @staticmethod
    def get_vargaussian(bins,sill,vrange,nugget=0):
        gamma = numpy.zeros_like(bins)
        ratio = bins[bins>0]/vrange
        gamma[bins>0] = nugget+(sill-nugget)*(1-numpy.exp(-3*ratio**2))
        return gamma

    @staticmethod
    def get_varholeeffect(bins,sill,vrange,nugget=0):
        gamma = numpy.zeros_like(bins)
        ratio = bins[bins>0]/vrange
        gamma[bins>0] = nugget+(sill-nugget)*(1-numpy.sin(ratio)/ratio)
        return gamma

    @staticmethod
    def get_varcubic(bins,sill,vrange,nugget=0):
        gamma = numpy.zeros_like(bins)
        ratio = bins[bins>0]/vrange
        gamma[bins>0] = nugget+(sill-nugget)*(7*ratio**2-35/4*ratio**3+7/2*ratio**5-3/4*ratio**7)
        gamma[bins>vrange] = sill
        return gamma

    @staticmethod
    def get_varcauchy(bins,sill,vrange,nugget=0):
        gamma = numpy.zeros_like(bins)
        ratio = bins[bins>0]/vrange
        gamma[bins>0] = nugget+(sill-nugget)*(1-1/(1+ratio**2))
        return gamma

    @staticmethod
    def get_vardewijs(bins,sill,nugget=0):
        gamma = numpy.zeros_like(bins)
        gamma[bins>0] = nugget+(sill-nugget)*numpy.log(bins[bins>0])
        return gamma

if __name__ == "__main__":

    import matplotlib.pyplot as plt
    import numpy as np

    A = variogram([1,2,3,4],x=[0.1,0.2,0.3,0.4])

    print(A.distmat)

    h = np.linspace(0,40,1000)

    c = 1
    a = 10
    nugget = 0.1

    gamma1 = A.get_varpower(h,c,p=0.2,nugget=nugget)
    gamma2 = A.get_varspherical(h,c,a,nugget=nugget)
    gamma3 = A.get_varexponential(h,c,a,nugget=nugget)
    gamma4 = A.get_vargaussian(h,c,a,nugget=nugget)
    gamma5 = A.get_varholeeffect(h,c,a,nugget=nugget)
    gamma6 = A.get_varcubic(h,c,a,nugget=nugget)
    gamma7 = A.get_varcauchy(h,c,a,nugget=nugget)
    gamma8 = A.get_vardewijs(h,c,nugget=nugget)

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


from matplotlib import pyplot

import numpy

from scipy.stats import norm

class DykstraParson():
    """
    Calculates Dykstra-Parson coefficient for permeability and
    thickness (optional) values.

    If thickness values are not provided the permeability values
    are taken equiprobable.

    coeff : Dykstra-Parson coefficient
        zero for homogeneous reservoirs
        one for hypothetical infinitely heterogeneous reservoir

    In general, Dykstra-Parson and Lorenz coefficient are not equal each other.

    """

    def __init__(self,permeability,thickness=None):
        """Initialization:
        
        permeability : permeability of layers

        thickness : thickness of layers,
            None if layers have the same thickness
            list or array if layers have different thickness

        """

        self.permeability = numpy.array(permeability)

        if thickness is None:
            self.thickness = None
        else:
            self.thickness = numpy.array(thickness)

        self._solve()

    def _solve(self):

        indices = numpy.argsort(self.permeability)

        self._permeability = self.permeability[indices]

        if self.thickness is not None:
            self._thickness = self.thickness[indices]

        if self.thickness is None:
            probability = numpy.full(self.permeability.shape,1/self.permeability.size)
        else:
            probability = self._thickness/numpy.sum(self._thickness)

        cumprob = numpy.cumsum(probability)-probability/2

        self._ppf = norm.ppf(cumprob)

        self._slope,self._intercept = numpy.polyfit(
            self._ppf,numpy.log10(self._permeability),1)

        k50_0 = 10**(self._slope*norm.ppf(0.5)+self._intercept)
        k15_9 = 10**(self._slope*norm.ppf(0.159)+self._intercept)

        self._coeff = (k50_0-k15_9)/k50_0

    def view(self,axis=None):

        showFlag = True if axis is None else False

        if axis is None:
            figure,axis = pyplot.subplots(nrows=1,ncols=1)

        axis.scatter(self._ppf,self._permeability)
        axis.set_yscale('log')

        xaxis = axis.get_xlim()

        x_abs = max([abs(x) for x in xaxis])

        xaxis = numpy.array([-x_abs,x_abs])

        ybest = self._slope*xaxis+self._intercept

        axis.plot(xaxis,10**ybest,'k')

        axis.set_xlabel("Normal Quantiles")

        axis.set_ylabel("Log10(Permeability)")

        axis.grid(which="both")

        if showFlag:
            pyplot.show()

    @property
    def ppf(self):

        return self._ppf
    
    @property
    def slope(self):

        return self._slope

    @property
    def intercept(self):

        return self._intercept

    @property
    def coeff(self):

        return self._coeff

class Lorenz():
    """
    Calculates Lorenz coefficient for permeability, porosity and
    thickness values.

    If thickness values are not provided the thickness values
    assumed to be the same.

    coeff : Lorenz coefficient
        zero for perfect equality, homogeneous reservoirs
        one for perfect inequality, infinitely heterogeneous reservoirs

    In general, Dykstra-Parson and Lorenz coefficient are not equal each other.

    """

    def __init__(self,permeability,porosity,thickness=None):
        """
        permeability: permeability of layers representing flow capacity

        porosity: porosity of layers representing storage capacity

        thickness : thickness of layers,
            None if layers have the same thickness
            list or array if layers have different thickness

        """

        self.permeability = numpy.array(permeability)
        self.porosity = numpy.array(porosity)
        
        if thickness is None:
            self.thickness = None
        else:
            self.thickness = numpy.array(thickness)

        self._solve()

    def _solve(self):

        indices = numpy.flip(self.permeability.argsort())

        self._permeability = self.permeability[indices]
        self._porosity = self.porosity[indices]

        if self.thickness is None:
            self._thickness = 1
        else:
            self._thickness = self.thickness[indices]

        self._flowcapacity = self._permeability*self._thickness
        self._storagecapacity = self._porosity*self._thickness

        self._flowfraction = numpy.cumsum(self._flowcapacity)/numpy.sum(self._flowcapacity)
        self._storagefraction = numpy.cumsum(self._storagecapacity)/numpy.sum(self._storagecapacity)

        self._flowfraction = numpy.insert(self._flowfraction,0,0)
        self._storagefraction = numpy.insert(self._storagefraction,0,0)

        area = numpy.trapz(self._flowfraction,self._storagefraction)
        
        self._coeff = (area-0.5)/0.5

    def view(self,axis=None):

        showFlag = True if axis is None else False

        if axis is None:
            figure,axis = pyplot.subplots(nrows=1,ncols=1)

        axis.plot(self._storagefraction,self._flowfraction,color='k',linewidth=0.5)

        for sfrac,ffrac in zip(self._storagefraction,self._flowfraction):
            axis.vlines(sfrac,ymin=sfrac,ymax=ffrac,color='k',linewidth=0.5)

        axis.scatter(self._storagefraction,self._flowfraction,s=10,zorder=3)

        axis.plot((0,1),(0,1),color='red')
        
        axis.fill_between(
            x = self._storagefraction,
            y1 = self._storagefraction,
            y2 = self._flowfraction,
            facecolor = "gray",
            alpha = 0.2)

        axis.set_xlim((0,1))
        axis.set_ylim((0,1))

        axis.set_xlabel("Fraction of Total Storage Capacity")
        axis.set_ylabel("Fraction of Total Flow Capacity")

        if showFlag:
            pyplot.show()

    @property
    def coeff(self):

        return self._coeff

    @property
    def storagefraction(self):

        return self._storagefraction

    @property
    def flowfraction(self):
        
        return self._flowfraction
    
    
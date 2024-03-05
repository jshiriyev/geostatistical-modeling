import numpy

from scipy.stats import norm

from gmodel.utils._spatial import Spatial

from gmodel.gstats._variogram import Variogram

class Kriging():

    @staticmethod
    def simple(obsdata:Spatial,estdata:Spatial,mean:float=None):

        if mean is None:
            self.mean = obsdata.mean()
        else:
            self.mean = mean
        
        "perc -> percentile, perc=0.5 gives mean values"

        self.distance = estdata.distmat(obsdata)
        
        _,self.covariance = SpatProp.get_varmodel(
            self.distance,self.obs.type,
            self.obs.sill,self.obs.range,
            self.obs.nugget)

        self.lambdas = numpy.linalg.solve(self.obs.covariance,self.covariance)
        
        calc_diff_arr = self.obs.reshape((-1,1))-self.mean
        calc_prop_mat = self.lambdas*(calc_diff_arr)
        calc_vars_mat = self.lambdas*self.covariance
        
        estimate = self.mean+calc_prop_mat.sum(axis=0)
        variance = self.obs.sill-calc_vars_mat.sum(axis=0)

        return estimate,variance

    @staticmethod
    def ordinary(obsdata:Spatial,estdata:Spatial):
        """perc -> percentile, perc=0.5 gives mean values"""

        self.distance = estdata.distmat(obsdata)
        
        _,self.covariance = SpatProp.get_varmodel(
            self.distance,self.obs.type,
            self.obs.sill,self.obs.range,
            self.obs.nugget)
        
        Am = self.var.covariance
        Ar = numpy.ones(Am.shape[0]).reshape((-1,1))
        Ab = numpy.ones(Am.shape[0]).reshape((1,-1))
        Ab = numpy.append(Ab,numpy.array([[0]]),axis=1)
        Am = numpy.append(Am,Ar,axis=1)
        Am = numpy.append(Am,Ab,axis=0)

        bm = self.covariance
        bb = numpy.ones(bm.shape[1]).reshape((1,-1))
        bm = numpy.append(bm,bb,axis=0)

        xm = numpy.linalg.solve(Am,bm)
        
        self.lambdas = xm[:-1,:]
        self.beta = xm[-1,:]

        calc_prop_mat = self.lambdas*self.obs.reshape((-1,1))
        calc_vars_mat = self.lambdas*self.covariance

        estimate = calc_prop_mat.sum(axis=0)
        variance = self.sill-self.beta-calc_vars_mat.sum(axis=0)

        return estimate,variance

    @staticmethod
    def percentile(estimate,variance,perc=0.5):
        """perc -> percentile, perc=0.5 gives mean values"""
        return estimate+norm.ppf(perc)*numpy.sqrt(variance)
"""
Code to generate simulated X-ray spectra for an active galactic nuclei. 970 photon rate/energy pairs are generated between 0.3-10 keV.
See the original paper for details on how parameters of the AGN were selected. 
Citations:
xspec: Arnaud, K.A., 1996, Astronomical Data Analysis Software and Systems V, eds. Jacoby G. and Barnes J., p17, ASP Conf. Series volume 101.
"""
import sys
import xspec
import matplotlib.pyplot as plt
import random
import math
import pickle
import os
import warnings

#The RMF and ARF names
rmf_list = ['rmf_arf/rmfs/swxpc0to12s0_20010101v010.rmf', 'rmf_arf/rmfs/swxpc0to12s6_20010101v010.rmf']
arf_list = ['ESO242G008','Mkn1044','Mkn1048','MRk335','MS0117-28','QSO005636', 'RXJ0100.4-5113', 'RXJ0105.6-1416','RXJ0117.5-3826'
       ,'RXJ0128.1-1848','RXJ0134.2-4258','RXJ0136.9-3510','RXJ0148.3-2758','RXJ0152.4-2319','TonS180']

class generator:
    def __init__(self, rmf_list, arf_list):
        self.rmf_list = rmf_list
        self.arf_list = arf_list
        #Defines all parameter limits (as laid out in paper)
        self.mass_min = 2
        self.mass_max = 450
        self.dist_min = 65
        self.dist_max = 6000
        self.logmdot_min = -1.65
        self.logmdot_max = 0.39
        self.astar_min = 0.5
        self.astar_max = .998
        self.i_min = 10
        self.i_max = 50
        self.redshift_min = 0.002
        self.redshift_max = 0.349
        self.exposure_time_min = 2000
        self.exposure_time_max = 20000
        #For testing purposes
        self.test = False
        
    def __rmf_picker(self):
        """
        Randomly selects an rmf to use.

        Returns
        -------
        self.rmf_list[number]: str
            Relative path to the chosen rmf.
            
        number: int
            Numerical representation of rmf
        """
        number = random.randint(0,1)
        return self.rmf_list[number], number
    
    def __arf_picker(self):
        """
        Randomly selects an arf to use.
        
        Returns
        -------
        arf_location: str
            Relative path to the chosen arf.
            
        number: int
            Numerical representation of arf
        """
        number = random.randint(0,14)
        arf_type = self.arf_list[number]
        arf_location = 'rmf_arf/' + arf_type + '/' +arf_type + 'pc.arf'
        return arf_location, number
    
    def __param_selector(self):
        """
        Randomly selects and normalizes the 6 key parameters in the
        QSOSED model.

        Returns
        -------
        mass : int
            Unnormalized value of the AGN mass in solar masses.
        dist : int
            Unnormalized value of the distance of the AGN from Earth in Mpc.
        logmdot : float
            Unnormalized value of the logarithm of the accretion rate. Dimensionless.
        astar : float
            Unnormalized value of the dimensionless black hole spin.
        cosi : float
            Unnormalized value of the cosine of the inclination angle of the accretion disk.
        redshift : float
            Unnormalized value of the dimensionless redshift.
        exposure_time : int
            The hypothetical exposure time of the AGN observation in seconds.
        normalized_labels : list
            Normalized values of the above 6 parameters of the QSOSED model.
        """
        mass = random.randint(self.mass_min,self.mass_max)*10**6
        #How to constrain distance 
        dist = random.randint(self.dist_min,self.dist_max) #Used to be 100,10000
        #Check the allowed values by XSPEC
        logmdot = random.uniform(self.logmdot_min,self.logmdot_max)
        #Used that astar tends to relatively large among Seyfert 1 Galaxies. Will likely have very little impact on findings
        astar = random.uniform(self.astar_min,self.astar_max)
        #Inclination is typically low in Seyfert 1. Make sure this is in degrees NOT radians
        i = random.randint(self.i_min,self.i_max)
        i_rad = math.radians(i)
        cosi = math.cos(i_rad)
        #Constrained by the 92
        redshift = random.uniform(self.redshift_min,self.redshift_max)
        #Constrained by the 15
        exposure_time = random.randint(self.exposure_time_min,self.exposure_time_max)
        normalized_labels = self.__normalizer(mass, dist, logmdot, astar, cosi, redshift)
        return mass, dist, logmdot, astar, cosi, redshift, exposure_time, normalized_labels

    def __normalizer(self, mass, dist, logmdot, astar, cosi, redshift):
        """
        Normalizes the 6 key parameters in the
        QSOSED model.

        Parameters
        -------
        mass : int
            Unnormalized value of the AGN mass in solar masses.
        dist : int
            Unnormalized value of the distance of the AGN from Earth in Mpc.
        logmdot : float
            Unnormalized value of the logarithm of the accretion rate. Dimensionless.
        astar : float
            Unnormalized value of the dimensionless black hole spin.
        cosi : float
            Unnormalized value of the cosine of the inclination angle of the accretion disk.
        redshift : float
            Unnormalized value of the dimensionless redshift.
            
        Returns
        -------
        normalized_labels : list
            Normalized values of the above 6 parameters of the QSOSED model.
        """
        if type(mass) != int or type(dist) != int or type(logmdot) != float or type(astar) != float or type(cosi) != float or type(redshift) != float:
            raise TypeError("Parameters are not of the correct type! Mass and Distance need to be integers, all others should be floats")
        mass_normalized = (mass-self.mass_min*10**6)/((self.mass_max-self.mass_min)*10**6)
        dist_normalized = (dist-self.dist_min)/(self.dist_max-self.dist_min)
        logmdot_normalized = (logmdot-self.logmdot_min)/(self.logmdot_max-self.logmdot_min)
        astar_normalized = (astar-self.astar_min)/(self.astar_max-self.astar_min)
        cosi_normalized = (cosi - math.cos(math.radians(self.i_max)))/(math.cos(math.radians(self.i_min))-math.cos(math.radians(self.i_max)))
        redshift_normalized = (redshift-self.redshift_min)/(self.redshift_max-self.redshift_min)
        norm_params = [mass_normalized, dist_normalized, logmdot_normalized, astar_normalized, cosi_normalized, redshift_normalized]
        if any(value < 0 for value in norm_params) or any(value > 1 for value in norm_params):
            raise ValueError("Parameters are out of bounds or Normalization limits have not been updated!")
        return norm_params

    def __xspec_data_retriever(self, mass, dist, logmdot, astar, cosi, redshift, nSpectra, rmf, arf, exposure_time, counter):
        """
        Interfaces with XSPEC and generates the energies and rates for an AGN with given parameters.

        Parameters
        -------
        mass : int
            Unnormalized value of the AGN mass in solar masses.
        dist : int
            Unnormalized value of the distance of the AGN from Earth in Mpc.
        logmdot : float
            Unnormalized value of the logarithm of the accretion rate. Dimensionless.
        astar : float
            Unnormalized value of the dimensionless black hole spin.
        cosi : float
            Unnormalized value of the cosine of the inclination angle of the accretion disk.
        redshift : float
            Unnormalized value of the dimensionless redshift.
            
        Returns
        -------
        energies : list
            970 energy values evenly spaced between 0.3-10 keV.
        rates : list
            970 counts per second per keV associated with the a corresponding energy from
            the above list of values.
        errors : list
            A nested list containing lists of the error on the energy and rate, along with
            a list of the values of the QSOSED model at each of the respective energy
            values.
        """
        params = [mass, dist, logmdot, astar, cosi, redshift, nSpectra, exposure_time]
        for elems in params:
            if type(elems) != int and type(elems) != float:
                raise TypeError("Parameters need to be numbers!") 
        if mass < self.mass_min*10**6 or mass > self.mass_max*10**6 or dist < self.dist_min or dist > self.dist_max  or logmdot < self.logmdot_min or logmdot > self.logmdot_max  or astar < self.astar_min or astar > self.astar_max  or cosi > math.cos(math.radians(self.i_min)) or cosi < math.cos(math.radians(self.i_max))  or redshift < self.redshift_min or redshift > self.redshift_max  or exposure_time < self.exposure_time_min or exposure_time > self.exposure_time_max:
            raise ValueError("Parameters are out of defined bounds!")
        xspec.Xset.chatter = -100
        xspec.Xset.logChatter = -100
        data = xspec.AllData
        xspec.Model("qsosed", setPars = {1:mass,2:dist,3:logmdot,4:astar,5:cosi,6:redshift})
        fake1= xspec.FakeitSettings(response=rmf, arf=arf, exposure= exposure_time,
                    correction = 1, fileName = str(counter)+'.fak')
        data.fakeit(nSpectra, nSpectra*[fake1], noWrite=True)
        #Ignores everything below 0.3 keV
        data.ignore("1:1-29") 
        xspec.Plot.device = '/cps'
        xspec.Plot.xAxis= "keV"
        xspec.Plot.xLog = True
        xspec.Plot.yLog = True
        #xspec.Plot.show()
        xspec.Plot('data')
        energies = xspec.Plot.x()
        rates = xspec.Plot.y()
        energy_err = xspec.Plot.xErr()
        rate_err = xspec.Plot.yErr()
        modvals = xspec.Plot.model()
        xspec.AllData.clear()
        xspec.AllModels.clear()
        return energies, rates, [energy_err, rate_err, modvals]

    def looper(self, num_of_iterations):
        """
        Outward facing function which generates a given number of AGN spectra.
        
        Parameters
        -------
        num_of_iterations : int
            Number of spectra to generate.
            
        Returns
        -------
        answers : list
            Y data for NN.
        inputs : list
            X data for NN.
        uncertainties : list
            Uncertainty data for NN.
        """
        if type(num_of_iterations) != int and type(num_of_iterations) != float:
                raise TypeError("Parameters need to be numbers!") 
        if num_of_iterations > 10000:
            warnings.warn("For large num_of_iterations, can cause memory errors")
        answers = [0]*num_of_iterations
        inputs = [0]*num_of_iterations
        uncertainties = [0]*num_of_iterations
        counter = 0
        nSpectra = 1
        if self.test:
            xspec.Xset.seed = 1
            if num_of_iterations > 10000:
                return
        for i in range(num_of_iterations):
            #Pick RMF,ARF
            rmf, rmf_number = self.__rmf_picker()
            rmf = "build/" + rmf
            arf, arf_number = self.__arf_picker()
            arf = "build/"+ arf
            #Define Parameters
            mass, dist, logmdot, astar, cosi, redshift, exposure_time, normalized_labels = self.__param_selector()
            energies, rates, uncertainty_list = self.__xspec_data_retriever(mass, dist, logmdot, astar, cosi,
                                                   redshift, nSpectra, rmf, arf, exposure_time,
                                                   counter)
            #Ensure data is bright enough
            while sum(rates)/exposure_time < 0.001:
                mass, dist, logmdot, astar, cosi, redshift, exposure_time, normalized_labels = self.__param_selector()
                energies, rates, uncertainty_list = self.__xspec_data_retriever(mass, dist, logmdot, astar, cosi,
                                                       redshift, nSpectra, rmf, arf, exposure_time,
                                                       counter)
            answers[i] = normalized_labels
            energies.extend(rates)
            energies.append(rmf_number)
            energies.append(arf_number)
            energies.append(exposure_time-self.exposure_time_min/(self.exposure_time_max-self.exposure_time_min))
            inputs[i] = energies
            uncertainties[i] = uncertainty_list
        return answers, inputs, uncertainties

    def plotter(x,y):
        """
        Creates a scatter plot.
        
        Parameters
        -------
        x : list
            x data to plot.

        y : list
            y data to plot.   
        """
        plt.scatter(x,y)
        plt.show()
        return

    def saver(self, answers, inputs, uncertainties, number):
        """
        Saves the lists to the disk. 
        
        Parameters
        -------
        answers : list
            Y data for NN.
        inputs : list
            X data for NN.
        uncertainties : list
            Uncertainty data for NN.
        number : int
            Concatenated to list title to distinguish saved files. Increase as necessary
            
        """
        if type(answers) != list or type(inputs) != list or type(uncertainties) != list or type(uncertainties[0]) != list or type(uncertainties[1]) != list or type(uncertainties[2]) != list:
            raise TypeError("answers, inputs need to be lists, and uncertainties should be a nested list containing three lists!") 
        #Check length of lists (https://stackoverflow.com/questions/35791051/better-way-to-check-if-all-lists-in-a-list-are-the-same-length)
        all_list = [answers, inputs, uncertainties[0], uncertainties[1], uncertainties[2]]
        loop = iter(all_list)
        list_len = len(next(loop))
        if not all(len(x) == list_len for x in loop):
             raise ValueError('All lists (answers, inputs, and all lists in uncertainties) must have the same length!')         
        if len(uncertainties) != 3:
            raise ValueError('uncertainties list should contain exactly 3 lists')
        for lists in all_list:
            for vals in lists:
                if type(vals) != int and type(vals) != float:
                    raise ValueError("All elements of given list must be numerical!")
        with open('label'+str(number), "wb") as f:
            pickle.dump(answers, f)
        with open('inputs'+str(number), "wb") as f:
            pickle.dump(inputs, f)
        with open('uncertainties'+str(number), 'wb') as f:
            pickle.dump(uncertainties,f)
        return
        
#Run Script:
##num_of_iterations = 300
##gen = generator(rmf_list, arf_list)
##answers, inputs, uncertainties = gen.looper(num_of_iterations)


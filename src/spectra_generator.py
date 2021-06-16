"""
Code to generate simulated X-ray spectra for an active galactic nuclei. 970 photon rate/energy pairs are generated between 0.3-10 keV.
See the original paper for details on how parameters of the AGN were selected. 
Citations:
xspec: Arnaud, K.A., 1996, Astronomical Data Analysis Software and Systems V, eds. Jacoby G. and Barnes J., p17, ASP Conf. Series volume 101.
"""

import xspec
import matplotlib.pyplot as plt
import random
import math
import pickle

#The RMF and ARF names
rmf_list = ['rmf_arf/Extracted_From_Calb/swxpc0to12s0_20010101v010.rmf', 'rmf_arf/Extracted_From_Calb/swxpc0to12s6_20010101v010.rmf']
arf_list = ['ESO242G008','Mkn1044','Mkn1048','MRk335','MS0117-28','QSO005636', 'RXJ0100.4-5113', 'RXJ0105.6-1416','RXJ0117.5-3826'
       ,'RXJ0128.1-1848','RXJ0134.2-4258','RXJ0136.9-3510','RXJ0148.3-2758','RXJ0152.4-2319','TonS180']

class generator:
    def __init__(self, rmf_list, arf_list):
        self.rmf_list = rmf_list
        self.arf_list = arf_list
        
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
        mass = random.randint(2,450)*10**6
        #How to constrain distance 
        dist = random.randint(65,6000) #Used to be 100,10000
        #Check the allowed values by XSPEC
        logmdot = random.uniform(-1.65, .39)
        #Used that astar tends to relatively large among Seyfert 1 Galaxies. Will likely have very little impact on findings
        astar = random.uniform(0.5,.998)
        #Inclination is typically low in Seyfert 1. Make sure this is in degrees NOT radians
        i = random.randint(10,50)
        i_rad = math.radians(i)
        cosi = math.cos(i_rad)
        #Constrained by the 92
        redshift = random.uniform(0.002,0.349)
        #Constrained by the 15
        exposure_time = random.randint(2000, 20000)
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
        mass_normalized = (mass-2*10**6)/((450-2)*10**6)
        dist_normalized = (dist-65)/(6000-65)
        logmdot_normalized = (logmdot+1.65)/(0.39+1.65)
        astar_normalized = (astar-.5)/(0.998-0.5)
        cosi_normalized = (cosi - math.cos(math.radians(50)))/(math.cos(math.radians(10))-math.cos(math.radians(50)))
        redshift_normalized = (redshift - 0.002)/(0.349-0.002)
        return [mass_normalized, dist_normalized, logmdot_normalized, astar_normalized, cosi_normalized, redshift_normalized]

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
        answers = [0]*num_of_iterations
        inputs = [0]*num_of_iterations
        uncertainties = [0]*num_of_iterations
        counter = 0
        nSpectra = 1
        for i in range(num_of_iterations):
            #Pick RMF,ARF
            rmf, rmf_number = self.__rmf_picker()
            arf, arf_number = self.__arf_picker()
            #Define Parameters
            mass, dist, logmdot, astar, cosi, redshift, exposure_time, normalized_labels = self.__param_selector()
            energies, rates, uncertainty_list = self.__xspec_data_retriever(mass, dist, logmdot, astar, cosi,
                                                   redshift, nSpectra, rmf, arf, exposure_time,
                                                   counter)
            #Ensure data is bright enough
            while sum(rates)/exposure_time < 0.001:
                mass, dist, logmdot, astar, cosi, redshift, exposure_time, normalized_labels = param_selector()
                energies, rates, uncertainty_list = xspec_data_retriever(mass, dist, logmdot, astar, cosi,
                                                       redshift, nSpectra, rmf, arf, exposure_time,
                                                       counter)
            answers[i] = normalized_labels
            energies.extend(rates)
            energies.append(rmf_number)
            energies.append(arf_number)
            energies.append(exposure_time)
            inputs[i] = energies
            uncertainties[i] = uncertainty_list
            counter = counter + 1
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
            Concatenated to list title. Increase as necessary
            
        """
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


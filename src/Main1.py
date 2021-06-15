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

rmf_list = ['rmf_arf/Extracted_From_Calb/swxpc0to12s0_20010101v010.rmf', 'rmf_arf/Extracted_From_Calb/swxpc0to12s6_20010101v010.rmf']
arf_list = ['ESO242G008','Mkn1044','Mkn1048','MRk335','MS0117-28','QSO005636', 'RXJ0100.4-5113', 'RXJ0105.6-1416','RXJ0117.5-3826'
       ,'RXJ0128.1-1848','RXJ0134.2-4258','RXJ0136.9-3510','RXJ0148.3-2758','RXJ0152.4-2319','TonS180']
#Randomly Select one of each for all the different files
def rmf_picker():
    number = random.randint(0,1)
    return rmf_list[number], number
def arf_picker():
    number = random.randint(0,14)
    arf_type = arf_list[number]
    arf_location = 'rmf_arf/' + arf_type + '/' +arf_type + 'pc.arf'
    if arf_type == 'ESO242G008':
        arf_location = 'rmf_arf/' + arf_type + '/' + 'MRk335' + 'pc.arf'
    if arf_type == "RXJ0134.2-4258":
        arf_location = 'rmf_arf/' + arf_type + '/' + 'RXJ0128.1-1848' + 'pc.arf'
    return arf_location, number
def param_selector():
    """
    Remove data for which there was no listed outcome
    Parameters
    ----------
    data_pc : Pandas Dataframe
        Dataset after being read into pandas and with the relevant titles.
    Returns
    -------
    data_mc : Pandas Dataframe
        Dataset with all entries having outcomes.
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
    normalized_labels = normalizer(mass, dist, logmdot, astar, cosi, redshift)
    return mass, dist, logmdot, astar, cosi, redshift, exposure_time, normalized_labels

def normalizer(mass, dist, logmdot, astar, cosi, redshift):
    mass_normalized = (mass-2*10**6)/((450-2)*10**6)
    dist_normalized = (dist-65)/(6000-65)
    logmdot_normalized = (logmdot+1.65)/(0.39+1.65)
    astar_normalized = (astar-.5)/(0.998-0.5)
    cosi_normalized = (cosi - math.cos(math.radians(50)))/(math.cos(math.radians(10))-math.cos(math.radians(50)))
    redshift_normalized = (redshift - 0.002)/(0.349-0.002)
    return [mass_normalized, dist_normalized, logmdot_normalized, astar_normalized, cosi_normalized, redshift_normalized]

def xspec_data_retriever(mass, dist, logmdot, astar, cosi, redshift, nSpectra, rmf, arf, exposure_time, counter):
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

def looper(num_of_iterations, nSpectra):
    answers = [0]*num_of_iterations
    inputs = [0]*num_of_iterations
    uncertainties = [0]*num_of_iterations
    counter = 0
    for i in range(num_of_iterations):
        #Pick RMF,ARF
        rmf, rmf_number = rmf_picker()
        arf, arf_number = arf_picker()
        #Define Parameters
        mass, dist, logmdot, astar, cosi, redshift, exposure_time, normalized_labels = param_selector()
        energies, rates, uncertainty_list = xspec_data_retriever(mass, dist, logmdot, astar, cosi,
                                               redshift, nSpectra, rmf, arf, exposure_time,
                                               counter)
        cts = 0
        if i % 10 == 0:
            print(i)
        while sum(rates)/exposure_time < 0.001:
            mass, dist, logmdot, astar, cosi, redshift, exposure_time, normalized_labels = param_selector()
            #Temporarily removed back, was causing some issues
            #back = "back.pha"
            energies, rates, uncertainty_list = xspec_data_retriever(mass, dist, logmdot, astar, cosi,
                                                   redshift, nSpectra, rmf, arf, exposure_time,
                                                   counter)
            cts +=1
            if cts%10==0:
                print('stuck')
                if cts%20 == 0:
                    print('mega_stuck')
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
    plt.scatter(x,y)
    plt.show()
    return

#Run Script:
num_of_iterations = 300
nSpectra = 1
answers, inputs, uncertainties = looper(num_of_iterations, nSpectra)
with open('testlabelsv2', "wb") as f:
    pickle.dump(answers, f)
with open('testinputsv2', "wb") as f:
    pickle.dump(inputs, f)
with open('uncertainties', 'wb') as f:
    pickle.dump(uncertainties,f)

    
#Scatter Plots them. Need to include x and y errors if possible
#plt.scatter(chans, rates)
#plt.show()
#plt.savefig('myplot')

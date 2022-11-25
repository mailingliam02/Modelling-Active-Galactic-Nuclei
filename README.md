# Modelling Active Galatic Nuclei using XSPEC and Neural Networks
## Introduction
This is a repository containing the python files used in my Durham University BSc Computing Project titled "Modelling an Active Galactic Nuclei using a Neural Network". The purpose of the project was to train a neural network on simulated active galactic nuclei (AGN) spectras to predict key components of the black hole like accretion rate and mass. This neural network was then generalized to real active galactic nuclei, and its performance compared against the predictions made by standard approaches.
The full paper can be read in the docs directory.

## How to Use
Ensure the appropriate dependencies are installed (see requirements.txt):
```
pip install -r requirements.txt
```
To generate simulated data:
```
python src/spectra_generator.py
```
To fit a neural network to real data:
```
python src/best_real_world.py
```
To fit a neural network to simulated data:
```
python src/best_simulation.py
```

## Data
The real spectral energy distributions used in the paper were accessed from the UK Swift Data Centre, and can be downloaded from this link: https://www.swift.ac.uk/swift_portal/. 
For the selected 29 AGNs, grades of 0-12 were used, the XRT was in photon-counting mode and the SED was normalized, consistent with the process used
by Grupe et al. [1]. The recommended single pass centroid method was used by the building software to further refine the coordinates of the source. As is standard for the XRT,the first 30 channels were ignored. The energies, countrate per energy, exposure time, and errors of the spectrum were then extracted using XSPEC, an X-ray spectral fitting package.

The simulated spectral energy distributions were generated using QSOSED, a model for predicting the spectral energy distribution of an active galactic nuclei. For more information about the model, please consult: https://heasarc.gsfc.nasa.gov/xanadu/xspec/manual/node132.html. The response matrix (RMF) and ancillary response matrix (ARF) files used in these simulations are available under the rmf_arf directory.

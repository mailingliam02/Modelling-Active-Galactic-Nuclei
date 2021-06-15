# Modelling Active Galatic Nuclei using XSPEC and Neural Networks
## Introduction
This is a repository containing the python files used in the "Modelling an Active Galactic Nuclei using a Neural Network" paper (see docs for full paper pdf). The purpose of the project was to train a neural network on simulated active galactic nuclei (AGN) spectras to predict key components of the black hole like accretion rate and mass. This neural network would then be generalized to real active galactic nuclei.

## How to Use
Download the latest data from https://github.com/beoutbreakprepared/nCoV2019 and extract and place latestdata.csv in the root directory. For Windows, this can be done by typing in the following after navigating to the cv19_mortalityrisk_predictors folder:
```
curl https://raw.githubusercontent.com/beoutbreakprepared/nCoV2019/master/latest_data/latestdata.tar.gz --output  latestdata.tar.gz
tar -xvzf .\latestdata.tar.gz -C .
```
Ensure the appropriate dependencies are installed (see requirements.txt):
```
pip install -r requirements.txt
```
Navigate to the build directory and execute script to clean dataset and generate results:
```
cd build
main.bat
```
Review the results txt which is generated in the build directory, and adjust hyperparameters as necessary (see paper for exact configurations used). 
Note that the execution of the above script can be quite lengthy due to the large range of the Grid Searches employed. To reduce the length of the script, adjust the size of the gridsearch in svm.py and rf.py in src.

## Results
The Random Forest was found to be the best predictor with an accuracy of 95%, although it is noted that none of the models were particularly effective at predicting the death of a patient. This is attributed to the sampling technique used. See the paper for details about implementation choices and results.
Table containing performance metrics for each of the different classifiers:

![tablef](https://user-images.githubusercontent.com/71287923/120115746-6983f980-c185-11eb-9aa9-4ecc8ac60b2e.PNG)


Plot of recall vs precision for each of the five trials of the classifier:

![precvsrecall1](https://user-images.githubusercontent.com/71287923/120115714-4a856780-c185-11eb-85f2-562366255b4a.png)

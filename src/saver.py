import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras import losses
from tensorflow.keras import preprocessing
import matplotlib.pyplot as plt
import numpy as np
import pickle
import os
import math
import datetime
import itertools
import copy
import random

class preprocessing:
    def __init__(self, number):
        self.labels = pickle.load(open("label"+str(number)), "rb")
        self.inputs = pickle.load(open("inputs"+str(number)), "rb")
        self.__setup()

    def __normalize(self):
        
                






for _, __, files in os.walk("./build"):
    file_list = files
for files in file_list:
    if files[0:5] == "label" and files[5:].isdigit():

                
                
#HYPERPARAMETERS:
##inputs_train = pickle.load(open("inputs1","rb")) #List of Lists of [energies, rates, rmf_number, arf_number, exposure_time]
##print("Train Inputs 1 Loaded")
##labels_train = pickle.load(open("answers1","rb")) #List of Lists of [mass, dist, logmdot, astar, cosi, redshift]
##print("Train Labels 1 Loaded")
##inputs2_train = pickle.load(open("inputs2","rb")) #List of Lists of [energies, rates, rmf_number, arf_number, exposure_time]
##print("Train Inputs 2 Loaded")
##labels2_train = pickle.load(open("answers2","rb")) #List of Lists of [mass, dist, logmdot, astar, cosi, redshift]
##print("Train Labels 2 Loaded")
##inputs3_train = pickle.load(open("inputs3","rb")) #List of Lists of [energies, rates, rmf_number, arf_number, exposure_time]
##print("Train Inputs 3 Loaded")
##labels3_train = pickle.load(open("answers3","rb")) #List of Lists of [mass, dist, logmdot, astar, cosi, redshift]
##print("Train Labels 3 Loaded")
##inputs4_train = pickle.load(open("inputs4","rb")) #List of Lists of [energies, rates, rmf_number, arf_number, exposure_time]
####print("Train Inputs 4 Loaded")
##labels4_train = pickle.load(open("answers4","rb")) #List of Lists of [mass, dist, logmdot, astar, cosi, redshift]
##print("Train Labels 4 Loaded")
##inputs_train.extend(inputs2_train)
##labels_train.extend(labels2_train)
##inputs_train.extend(inputs3_train)
##labels_train.extend(labels3_train)
##inputs_train.extend(inputs4_train)
##labels_train.extend(labels4_train)
##
##train_data_np = np.asarray(inputs_train)
##train_labels_np = np.asarray(labels_train)
##np.save("input1to4.npy", train_data_np)
####np.save("labels1to4.npy", train_labels_np)
##
inputs_train = pickle.load(open("inputs15","rb")) #List of Lists of [energies, rates, rmf_number, arf_number, exposure_time]
print("Train Inputs 1 Loaded")
labels_train = pickle.load(open("answers15","rb")) #List of Lists of [mass, dist, logmdot, astar, cosi, redshift]
print("Train Labels 1 Loaded")
##inputs2_train = pickle.load(open("inputs14","rb")) #List of Lists of [energies, rates, rmf_number, arf_number, exposure_time]
##print("Train Inputs 2 Loaded")
##labels2_train = pickle.load(open("answers14","rb")) #List of Lists of [mass, dist, logmdot, astar, cosi, redshift]
##print("Train Labels 2 Loaded")
##inputs3_train = pickle.load(open("inputs15","rb")) #List of Lists of [energies, rates, rmf_number, arf_number, exposure_time]
##print("Train Inputs 3 Loaded")
##labels3_train = pickle.load(open("answers15","rb")) #List of Lists of [mass, dist, logmdot, astar, cosi, redshift]
##print("Train Labels 3 Loaded")
####inputs4_train = pickle.load(open("inputs12","rb")) #List of Lists of [energies, rates, rmf_number, arf_number, exposure_time]
######print("Train Inputs 4 Loaded")
####labels4_train = pickle.load(open("answers12","rb")) #List of Lists of [mass, dist, logmdot, astar, cosi, redshift]
####print("Train Labels 4 Loaded")
##inputs_train.extend(inputs2_train)
##labels_train.extend(labels2_train)
##inputs_train.extend(inputs3_train)
##labels_train.extend(labels3_train)
####inputs_train.extend(inputs4_train)
####labels_train.extend(labels4_train)
##input_data = np.load("inputs1to15.npy", mmap_mode = "r")

recycle_number = 3

#Pre preprocessing
def make_real_world(input_data):
    for inputs in input_data:
        #Checked
        energy = inputs[:995]
        rates = inputs[995:1990]
        rest = inputs[1990:]
##        print(len(energy))
##        print(len(rates))
        data_points = random.randint(250,900)
        #Checked. Range list starts at 0
        list_to_remove = random.sample(range(995), data_points)
        list_to_remove.sort(reverse=True)
        i = 0
        for indices in list_to_remove:
            #Should work, as new indice will always be strictly smaller
            del energy[indices]
            energy.append(0)
            del rates[indices]
            rates.append(0)
        energy.extend(rates)
        energy.extend(rest)
        inputs = copy.deepcopy(energy)
    return input_data
        
recycled_inputs = make_real_world(inputs_train)
for i in range(recycle_number-1):
    recycle_holder = make_real_world(inputs_train)
    recycled_inputs.extend(recycle_holder)
    labels_train.extend(labels_train)
    
##recycled_test_inputs = make_real_world(inputs_test) #Only recycled once!
train_data_np = np.asarray(recycled_inputs)
train_labels_np = np.asarray(labels_train)
print("Successfully Recycled")

np.save("Inbetween/realinput15.npy", train_data_np)
np.save("Inbetween/reallabels15.npy", train_labels_np)




##
##def make_real_world_(input_data):
##    print(input_data)
####    for inputs in input_data:
##        #Checked
##    energy = inputs[:995]
##    rates = inputs[995:1990]
##    rest = inputs[1990:]
####        print(len(energy))
####        print(len(rates))
##    data_points = random.randint(250,900)
##    #Checked. Range list starts at 0
##    list_to_remove = random.sample(range(995), data_points)
##    list_to_remove.sort(reverse=True)
##    i = 0
##    for indices in list_to_remove:
##        #Should work, as new indice will always be strictly smaller
##        del energy[indices]
##        energy.append(0)
##        del rates[indices]
##        rates.append(0)
##    energy.extend(rates)
##    energy.extend(rest)
##    inputs = copy.deepcopy(energy)
##    return input_data
##
##for i in range(input_data.shape[0]):
##    input_data[i] = make_real_world_(input_data[i])
##train_data_np = np.asarray(inputs_train)
##train_labels_np = np.asarray(labels_train)
##np.save("input13to15.npy", train_data_np)
##np.save("label13to15.npy", train_labels_np)

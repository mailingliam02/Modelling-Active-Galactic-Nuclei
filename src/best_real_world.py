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
#HYPERPARAMETERS:
initial_learning_rate = 0.00001
n_neurons = 2048
h_neurons = 2048
h2_neurons = 2048
h3_neurons = 1024
h4_neurons = 1024
h5_neurons = 512
h6_neurons = 512
h7_neurons = 256
drp_rate1 = 0.1
drp_rate2 = 0.1
drp_rate3 = 0.1
drp_rate4 = 0.1
drp_rate5 = 0.1
drp_rate6 = 0.1
drp_rate7 = 0.1
recycle_number = 3
#Parameters
epochs = 1000
batch_size = 32
validation_split = .2

#Changes Working Directory to Right Place
os.chdir("/home/mailingliam/Computational_Project")
# Prepare a directory to store all the checkpoints.
checkpoint_dir = "./ckpt"
if not os.path.exists(checkpoint_dir):
    os.makedirs(checkpoint_dir)
###Loads inputs and outputs
inputs_test = pickle.load(open("inputs","rb")) #List of Lists of [energies, rates, rmf_number, arf_number, exposure_time]
print("Test Inputs Loaded")
labels_test = pickle.load(open("answers","rb")) #List of Lists of [mass, dist, logmdot, astar, cosi, redshift]
print("Test Labels Loaded")
test_data_np = np.asarray(inputs_test) #Curently not recycled, should maybe test?
test_labels_np = np.asarray(labels_test)

input_memmap = np.load("Inbetween/shuffled_final_12gb.npy", mmap_mode="r")
label_memmap = np.load("Inbetween/shuffled_final_12gb_answers.npy", mmap_mode="r")

#Validation Maps:
val_in_memmap = np.load("Inbetween/combined_real_inputs1.npy", mmap_mode="r")
val_out_memmap = np.load("Inbetween/combined_real_labels1.npy", mmap_mode="r")

print("Compiling")

def build_and_compile_fit_model(norm):
    dnn_model = tf.keras.Sequential([
        norm,
##        layers.Dropout(drp_rate1),
        layers.Dense(n_neurons,activation='relu', kernel_regularizer=tf.keras.regularizers.L2(0.00005)),# input_shape = (batch_size,1993,), 
        layers.Dropout(drp_rate2),
        layers.Dense(h_neurons, activation = 'relu', kernel_regularizer= tf.keras.regularizers.L2(0.00005)),
        layers.Dropout(drp_rate3),
        layers.Dense(h2_neurons, activation = 'relu', kernel_regularizer= tf.keras.regularizers.L2(0.00005)),
        layers.Dropout(drp_rate4),
        layers.Dense(h3_neurons, activation = 'relu', kernel_regularizer= tf.keras.regularizers.L2(0.00005)),
        layers.Dropout(drp_rate5),
        layers.Dense(h4_neurons, activation = 'relu', kernel_regularizer= tf.keras.regularizers.L2(0.00005)),
        layers.Dropout(drp_rate5),
        layers.Dense(h5_neurons, activation = 'relu', kernel_regularizer= tf.keras.regularizers.L2(0.00005)),
        layers.Dropout(drp_rate6),
        layers.Dense(h6_neurons, activation = 'relu', kernel_regularizer= tf.keras.regularizers.L2(0.00005)),
        layers.Dropout(drp_rate7),
        layers.Dense(h7_neurons, activation = 'relu'),
        layers.Dense(6, activation = 'sigmoid')
        ])
    dnn_model.compile(loss = 'mean_squared_error',
              optimizer = tf.keras.optimizers.Adam(learning_rate = initial_learning_rate),
              metrics = [tf.keras.metrics.MeanAbsoluteError()])
    dnn_model.summary()
    history = dnn_model.fit(
        input_memmap, label_memmap,
        validation_data = (val_in_memmap, val_out_memmap),
        verbose = 2, epochs = epochs, shuffle = True,
        callbacks = callbacks)
    return history, dnn_model


#Defines Callbacks (Saves Model)

log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

callbacks = [
    tf.keras.callbacks.ModelCheckpoint(
        filepath = checkpoint_dir+"_looper", save_best_only = True,  #Changed from Best, may cause a problem?
        monitor = "val_loss"
        ),
    tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1),
    tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5,
                              patience=30, min_lr=0.0000000005),
    tf.keras.callbacks.EarlyStopping(monitor = 'val_loss', patience = 150)
    ]

#Defines Normalizing Layer
normalizer = layers.experimental.preprocessing.Normalization()
#Adapts the Normalizing Layer to the Data (so it can normalize appropriately)
normalizer.adapt(input_memmap)
print("Time to Fit!")
history, dnn_model = build_and_compile_fit_model(normalizer)

results = dnn_model.evaluate(test_data_np, test_labels_np, verbose=0)
predictions = dnn_model.predict(test_data_np)
print("test loss, test acc:", results)
acc = history.history['mean_absolute_error']
val_acc = history.history['val_mean_absolute_error']
loss = history.history['loss']
val_loss = history.history['val_loss']

with open('loss', "wb") as f:
    pickle.dump(loss, f)
with open('val_loss', "wb") as f:
    pickle.dump(val_loss, f)



os.chdir("/home/mailingliam/Computational_Project/plots")
f = open("captains_log.txt","a")
f.write("\n")
f.write("["+str(initial_learning_rate)+", "+ str([n_neurons,h_neurons,h2_neurons])+", " + str([drp_rate2,drp_rate3])+", "+
        str(batch_size)+", "+str(epochs)+"]")
f.close()

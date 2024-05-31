#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tensorflow as tf
from tensorflow import keras

fashion_mnist = keras.datasets.fashion_mnist
(x_train, y_train),(x_test,y_test) = fashion_mnist.load_data()
x_train,x_test =x_train/255.0,x_test/255.0 #normalize the pixel values to be in [0,1]

#note we need to flatten the image to a vector, to serve as the input layer of the network

#1a: Select one image from each class fo the dataset to display as a grey-scale image






#2a: Give the recognition accuracy rate of the test set, and show the confusion matrix
 
 

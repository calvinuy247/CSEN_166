#!/usr/bin/env python3
import tensorflow as tf
from tensorflow import keras
from keras import datasets, layers, models
import numpy as np

#Loading the dataset
fashion_mnist = keras.datasets.fashion_mnist

#y_train = training labels || y_test = test labels
(x_train,y_train),(x_test,y_test) = fashion_mnist.load_data()

#Normalize the pixel values to be in [0,1]
x_train,x_test = x_train/255.0,x_test/255.0


#1a: Select one image from each class of the dataset to display as a grey-scale image
import matplotlib.pyplot as plt



plt.imshow(x_test[19,:,:], cmap='gray', vmin=0, vmax=1)
plt.show()
### Need to finish this section, going to see if there are any tips during lab intro. ###

#Setting the model
model = models.Sequential()


#Adding layers
#Note we need to flatten the image to a vector, to serve as the input layer of the network
model.add(layers.Flatten(28x28))

#Creating the hidden layer with 512 nodes and ReLU activation function
model.add(layers.Dense(512, activation='relu'))

#Creating the output layer with 10 nodes and softmax activation function
model.add(layers.Dense(10, activation='softmax'))


#Printing summary and compiling the model with adam optimizer and sparse... loss function  
model.summary()
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])


#Training the model for 5 epochs and a batch size of 32
model.fit(x_train, y_train, epochs=5, batch_size=32)


#Calculating the test's loss and accuracy
loss, accuracy = model.evaluate(x_test, y_test)
print(accuracy)


#Calculating the model's predicted probalilty 
predProbablility = model.predict(x_test)

#y_test_hat = predicted value, using argmax() to find the class with the highest probability
y_test_hat = np.argmax(predProbablility, axis=1)

#2a: Give the recognition accuracy rate of the test set, and show the confusion matrix
from sklearn.metrics import confusion_matrix

### Also need to finish this section. ###
#Need to replace the ... with labels, like in mnist_cnn.py 
#confuMatrix = confusion_matrix(y_test, y_test_hat, ...)
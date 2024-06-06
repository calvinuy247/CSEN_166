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

#Selecting an image from each class to display as a grey-scale image
import matplotlib.pyplot as plt
classes = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat", "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]

#Stores an image for each class
imagesEachClass = {}

#Traversing every image in the test dataset
for image in range(len(x_test)):
    #Getting the label for the current image
    label = y_test[image]

    if label not in imagesEachClass:
        imagesEachClass[label] = x_test[image]
    if len(imagesEachClass) == 10:
        #Stopping at 10 because only 10 classes
        break

#Creating and formatting the images
plt.figure(figsize=(10,10))
for image in range(10):
    plt.subplot(1, 10, image+1)
    plt.xticks([]) #Removing X-axis tick marks
    plt.yticks([]) #Removing Y-axis tick marks
    plt.grid(False) #Removing the grid lines
    plt.imshow(imagesEachClass[image], cmap='gray', vmin=0, vmax=1)
    plt.xlabel(classes[image])
plt.show()

#Setting the model
model = models.Sequential()

#Adding layers
#Note we need to flatten the image to a vector, to serve as the input layer of the network
model.add(layers.Flatten())

#Creating the hidden layer with 512 nodes and ReLU activation function
model.add(layers.Dense(512, activation='relu'))

#Creating the output layer with 10 nodes and softmax activation function
model.add(layers.Dense(10, activation='softmax'))

#Printing summary and compiling the model with adam optimizer and sparse... loss function  
model.summary()
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

#Training the model for 5 epochs and a batch size of 32
model.fit(x_train, y_train, epochs=5, batch_size=32)

#Calculating the model's predicted probalilty 
predProbablility = model.predict(x_test)

#y_test_hat = predicted value, using argmax() to find the class with the highest probability
y_test_hat = np.argmax(predProbablility, axis=1)

#Calculating the test's loss and accuracy
loss, accuracy = model.evaluate(x_test, y_test)
print(accuracy)

#Creating and plotting the confusion matrix
from sklearn.metrics import ConfusionMatrixDisplay
ConfusionMatrixDisplay.from_predictions(y_test, y_test_hat)
plt.show()

#Printing the model summary
model.summary()
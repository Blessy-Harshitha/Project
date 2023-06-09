

Skip to content
Using RGUKT Mail with screen readers

Conversations
Using 0.44 GB
Program Policies
Powered by Google
Last account activity: 15 hours ago
Details
import pandas as pd
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns

DATASET="train"
DATASET2="valid"

CATEGORIES=["Tomato___Bacterial_spot","Tomato___Early_blight","Tomato___healthy","Tomato___Late_blight","Tomato___Leaf_Mold","Tomato___Septoria_leaf_spot","Tomato___Spider_mites Two-spotted_spider_mite","Tomato___Target_Spot","Tomato___Tomato_mosaic_virus","Tomato___Tomato_Yellow_Leaf_Curl_Virus"]
        
train_data=[]

for category in CATEGORIES:
        label=CATEGORIES.index(category)
        path=os.path.join(DATASET,category)#combines path names into one complete path
        for img_file in os.listdir(path):#to get the list of all files and directories in the specified directory.
            img=cv.imread(os.path.join(path,img_file),1)#loads img
            img=cv.cvtColor(img,cv.COLOR_BGR2RGB)#to convert an image from one color space to another (BGR is converted to RGB)
            img=cv.resize(img,(64,64))            
            train_data.append([img,label])
            
test_data=[]

for category in CATEGORIES:
        label=CATEGORIES.index(category)
        path=os.path.join(DATASET2,category)
        for img_file in os.listdir(path):
            img=cv.imread(os.path.join(path,img_file),1)
            img=cv.cvtColor(img,cv.COLOR_BGR2RGB)
            img=cv.resize(img,(64,64))
            test_data.append([img,label])
            
print(len(train_data))
print(len(test_data))

import random

random.shuffle(train_data)#to increase accuracy of a thing(overfitting)
random.shuffle(test_data)

for lbl in train_data[:10]:
    print(lbl[1])
    
X_train=[]
y_train=[]

for features,label in train_data:
    X_train.append(features)
    y_train.append(label)

Y=[]
for i in y_train:
    if i==0:
        Y.append("BACTERIAL SPOT")
    elif i==1:
        Y.append("EARLY BLIGHT")
    elif i==2:
        Y.append("HEALTHY")
    elif i==3:
        Y.append("LATE BLIGHT")
    elif i==4:
        Y.append("LEAF MOLD")
    elif i==5:
        Y.append("SEPTORIA LEAF SPOT")
    elif i==6:
        Y.append("SPIDER MITE")
    elif i==7:
        Y.append("TARGET SPOT")
    elif i==8:
        Y.append("MOSAIC VIRUS")
    else:
        Y.append("YELLOW LEAF CURL VIRUS")

len(X_train),len(y_train)

X_test=[]
y_test=[]

for features,label in test_data:
    X_test.append(features)
    y_test.append(label)
    
Z=[]
for i in y_test:
    if i==0:
        Z.append("BACTERIAL SPOT")
    elif i==1:
        Z.append("EARLY BLIGHT")
    elif i==2:
        Z.append("HEALTHY")
    elif i==3:
        Z.append("LATE BLIGHT")
    elif i==4:
        Z.append("LEAF MOLD")
    elif i==5:
        Z.append("SEPTORIA LEAF SPOT")
    elif i==6:
        Z.append("SPIDER MITE")
    elif i==7:
        Z.append("TARGET SPOT")
    elif i==8:
        Z.append("MOSAIC VIRUS")
    else:
        Z.append("YELLOW LEAF CURL VIRUS")

len(X_test),len(y_test)

X_train=np.array(X_train).reshape(-1,64,64,3)#Gives a new shape to an array without changing its data. reshape(-1) refers to an unknown dimension that the reshape() function calculates for you.
X_train=X_train/255.0 # Which standardizes all of the values in our training and testing sets.
X_train.shape #returns dimns and elements in array

X_test=np.array(X_test).reshape(-1,64,64,3)
X_test=X_test/255.0
X_test.shape

order=['BACTERIAL SPOT','EARLY BLIGHT','HEALTHY','LATE BLIGHT','LEAF MOLD','SEPTORIA LEAF SPOT','SPIDER MITE','TARGET SPOT','MOSAIC VIRUS','YELLOW LEAF CURL VIRUS']

ax=sns.countplot(Y, order=order) #Show the counts of observations in each categorical bin using bars.
ax.set_xlabel("Leaf Diseases")
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha='right') #the labels that you see next to each tick mark is ticklabels. ???????
ax.set_ylabel("Image Count")

ax=sns.countplot(Z, order=order)
ax.set_xlabel("Leaf Diseases")
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha='right') #for disease names rotation
ax.set_ylabel("Image Count")

from keras.utils import to_categorical #Converts a class vector (integers) to binary class matrix. data preproc????

one_hot_train=to_categorical(y_train) #Using the method to_categorical(), a numpy array (or) a vector which has integers that represent different categories, can be converted into a numpy array (or) a matrix which has binary values and has columns equal to the number of categories in the data
one_hot_train

one_hot_test=to_categorical(y_test)
one_hot_test

from tensorflow.keras.models import Sequential #A Sequential model is appropriate for a plain stack of layers where each layer has exactly one input tensor and one output tensor.
from tensorflow.keras.layers import Conv2D,Dense,Flatten,MaxPooling2D,Dropout
#2D convolution layer (e.g. spatial convolution over images.). By performing a spatial convolution an image can be transformed so that the pixel intensity represents the size of the gradient at the pixel location. 
#Dense layer is the regular deeply connected neural network layer.
#A Flatten layer in Keras reshapes the tensor to have a shape that is equal to the number of elements contained in the tensor. 
#MaxPooling2D: by taking the maximum value over an input window . The primary aim of a pooling operation is to reduce the size of the images as much as possible
#Dropout : The Dropout layer randomly sets input units to 0 with a frequency of rate at each step during training time, which helps prevent overfitting.

classifier=Sequential()#we will create an object of the sequential class below:

classifier.add(Conv2D(32,(3,3), input_shape=(64,64,3), activation='relu'))
classifier.add(MaxPooling2D(pool_size=(2,2)))
classifier.add(Dropout(0.2))

classifier.add(Conv2D(64,(3,3), activation='relu'))
classifier.add(MaxPooling2D(pool_size=(2,2)))
classifier.add(Dropout(0.2))

classifier.add(Conv2D(128,(3,3), activation='relu'))
classifier.add(MaxPooling2D(pool_size=(2,2)))
classifier.add(Dropout(0.4))

classifier.add(Flatten())

classifier.add(Dense(activation='relu', units=64))
classifier.add(Dense(activation='relu', units=128))
classifier.add(Dense(activation='relu', units=64))
classifier.add(Dense(activation='softmax', units=10))

classifier.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

classifier.summary() #The layers and their order in the model. The output shape of each layer.

hist=classifier.fit(X_train,one_hot_train,epochs=75,batch_size=128,validation_split=0.2) #Fraction of the training data to be used as validation data.

test_loss,test_acc=classifier.evaluate(X_test,one_hot_test)# check whether the model is best fit for the given problem and corresponding data.
test_loss,test_acc

plt.plot(hist.history['loss'])
plt.plot(hist.history['val_loss'])
plt.title('Classifier Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train','Validation'],loc='upper right')
plt.show()

plt.plot(hist.history['accuracy'])
plt.plot(hist.history['val_accuracy'])
plt.title('Classifier Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train','Validation'],loc='upper left')
plt.show()

y_pred=classifier.predict_classes(X_test) #provides the output classes for the parameter.
y_pred

y_prob=classifier.predict_proba(X_test)
y_prob

from sklearn.metrics import roc_curve, auc
#Compute Area Under the Receiver Operating Characteristic Curve (ROC AUC) from prediction scores.
#Compute Area Under the Curve (AUC) using the trapezoidal rule.
fpr = {}#False Positive Rate
tpr = {}#True Positive Rate
thresh ={}
roc_auc={}

n_class = 10

for i in range(n_class):    
    fpr[i], tpr[i], thresh[i] = roc_curve(y_test, y_prob[:,i], pos_label=i)#[:,i]????? returns which values??
    roc_auc[i] = auc(fpr[i], tpr[i])#?????
      
plt.plot(fpr[0], tpr[0], color='orange',label='Bacterial Spot AUC = %0.3f' % roc_auc[0])
plt.plot(fpr[1], tpr[1], color='green',label='Early Blight AUC = %0.3f' % roc_auc[1])
plt.plot(fpr[2], tpr[2], color='blue',label='Healthy AUC = %0.3f' % roc_auc[2])
plt.plot(fpr[3], tpr[3], color='red',label='Late Blight AUC = %0.3f' % roc_auc[3])
plt.plot(fpr[4], tpr[4], color='pink',label='Leaf Mold AUC = %0.3f' % roc_auc[4])
plt.plot(fpr[5], tpr[5], color='purple',label='Septoria Leaf Spot AUC = %0.3f' % roc_auc[5])
plt.plot(fpr[6], tpr[6], color='brown',label='Spider Mites AUC = %0.3f' % roc_auc[6])
plt.plot(fpr[7], tpr[7], color='cyan',label='Target Spot AUC = %0.3f' % roc_auc[7])
plt.plot(fpr[8], tpr[8], color='yellow',label='Mosaic Virus AUC = %0.3f' % roc_auc[8])
plt.plot(fpr[9], tpr[9], color='black',label='Yellow Leaf Curl Virus AUC = %0.3f' % roc_auc[9])
plt.title('Tomato Leaves Diseases ROC curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive rate')
plt.legend(loc='best')#legend() is used to specify the location of the legend.

from sklearn.metrics import confusion_matrix

sns.heatmap(confusion_matrix(y_test,y_pred))
cm=confusion_matrix(y_test,y_pred)
pro.py
Displaying pro.py.
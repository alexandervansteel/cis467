import cv2
import numpy as np
import os
from random import shuffle

TRAIN_DIR='./KDEF/'
TEST_DIR=''
IMG_SIZE=192

'''
Dimensions: 562 x 762

Letter 1: Session
    A = series one
    B = series two
Letter 2: Gender
    F = female
    M = male
Letter 3 & 4: Identity number
    01 - 35
Letter 5 & 6: Expression
    NE = neutral
    AF = afraid
    AN = angry
    DI = disgusted
    HA = happy
    SA = sad
    SU = surprised
Letter 7 & 8: Angle
    FL = full left profile
    HL = half left profile
    S = straight
    HR = half right profile
    FR = full right profile
'''

emotion_map = {'Neutral': 0,
               'Afraid': 1,
               'Angry': 2,
               'Disgust': 3,
               'Happy': 4,
               'Sad': 5,
               'Surprise': 6}

def label_image(img):
    word_label=img[4:7]
    if word_label=='NE':return 0 # neurtral
    if word_label=='AF':return 1 # afraid
    if word_label=='AN':return 2 # angry
    if word_label=='DI':return 3 # disgusted
    if word_label=='HA':return 4 # happy
    if word_label=='SA':return 5 # sad
    if word_label=='SU':return 6 # surprised

def create_train_data();
    training_data=[]
    for dirpath, dirname, filename in os.walk(TRAIN_DIR):
        for img in filename:
            label=label_image(img)
            path=os.path.join(TRAIN_DIR,img)
            img=cv2.imread(path,CV_LOAD_IMAGE_GRAYSCALE)
            if not img[6:9]=='FL' and not img[6:9]=='FR' : # remove full left and right images
                if (img.shape[0]>=img.shape[1]): # height is greater than width
                    resizeto=(IMG_SIZE,int(round(IMG_SIZE*(float(img.shape[1])/img.shape[0]))));
                else:
                    resizeto=(int(round(IMG_SIZE*(float(img.shape[0])/img.shape[1]))),IMG_SIZE);
                img=cv2.resize(img,(resizeto[1],resizeto[0]),interpolation=cv2.INTER_CUBIC)
                img=cv2.copyMakeBorder(img,0,IMG_SIZE-img.shape[0],0,IMG_SIZE-img.shape[1],cv2.BORDER_CONSTANT,0)
                training_data.append([np.array(img),np.array(label)])

    shuffle(training_data)
    np.save('train_data.npy',training_data)
    return training_data

def create_load_training_data(func):
    if func=='load':
        train_data=np.load('train_data.npy')
    else:
        train_data=create_train_data()

def process_test_data():
    testing_data=[]

    return testing_data

def split_training_data(training_data):
    train=training_data[:-499]
    test=training_data[-499:]

import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
'''
conv relu conv relu POOL conv relu conv relu POOL conv relu conv relu POOL FullConnected
'''
def create_model():
    model=Sequential()

    model.add(Conv2D(32,(5,5),padding='same',activation='relu',input_shape=(1,192,192))) # adjust input_shape to size of images
    model.add(Conv2D(32, (5, 5), padding='same', activation='relu'))
    model.add(Conv2D(32, (5, 5), padding='same', activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))

    model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
    model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
    model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))

    model.add(Conv2D(128, (3, 3), padding='same', activation='relu'))
    model.add(Conv2D(128, (3, 3), padding='same', activation='relu'))
    model.add(Conv2D(128, (3, 3), padding='same', activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))

    model.add(Flatten())

    model.add(Dense(128, activation='relu'))
    model.add(Dropout(.5))
    model.add(Dense(6, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    return model

model.fit(X_train,Y_train,verbose=2,shuffle=True,epochs=15,validation_split=.1)

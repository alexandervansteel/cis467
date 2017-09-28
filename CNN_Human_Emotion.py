import cv2
import numpy as np
import os
from random import shuffle

TRAIN_DIR='./KDEF/'
TEST_DIR=''

'''
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
def label_image(img):
    word_label=img[4:7]
    if word_label=='NE':return [1,0,0,0,0,0,0] # neurtral
    if word_label=='AF':return [0,1,0,0,0,0,0] # afraid
    if word_label=='AN':return [0,0,1,0,0,0,0] # angry
    if word_label=='DI':return [0,0,0,1,0,0,0] # disgusted
    if word_label=='HA':return [0,0,0,0,1,0,0] # happy
    if word_label=='SA':return [0,0,0,0,0,1,0] # sad
    if word_label=='SU':return [0,0,0,0,0,0,1] # surprised

def create_train_data();
    training_data=[]
    for dirpath, dirname, filename in os.walk(TRAIN_DIR):
        for img in filename:
            label=label_image(img)
            path=os.path.join(TRAIN_DIR,img)
            img=cv2.imread(path,CV_LOAD_IMAGE_GRAYSCALE)
            if not img[6:9]=='FL' and not img[6:9]=='FR' : # remove full left and right images
                training_data.append([np.array(img),np.array(label)])

    shuffle(training_data)
    np.save('train_data.npy',training_data)
    return training_data

def process_test_data():
    testing_data=[]

    return testing_data

import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv3D, MaxPooling2D
from keras import backend as K
'''
conv relu conv relu POOL conv relu conv relu POOL conv relu conv relu POOL FullConnected
'''
model=Sequential()
model.add(Conv3D())

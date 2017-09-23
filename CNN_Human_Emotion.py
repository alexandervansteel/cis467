import cv2
import numpy as np
import os
from random import shuffle

TRAIN_DIR=''
TEST_DIR=''

'''
7 Basic Emotions:
    anger
    contempt
    disgust
    Fear
    happy
    sadness
    suprise

'''
def label_image(img):

def create_train_data();
    training_data=[]
    for dirpath, dirname, filename in os.walk(TRAIN_DIR):
        for img in filename:
            label=label_image(img)
            path=os.path.join(TRAIN_DIR,img)
            img=cv2.imread(path,CV_LOAD_IMAGE_GRAYSCALE)
            training_data.append([np.array(img),np.array(label)])

    shuffle(training_data)
    np.save('train_data.npy',training_data)
    return training_data

def process_test_data():
    testing_data=[]

    return testing_data

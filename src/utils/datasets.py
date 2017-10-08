from scipy.io import loadmat
import pandas as pd
import numpy as np
from random import shuffle
import os
import cv2

class DataBaseManager(object):
    def _init_(self,dataset_name='KDEF',dataset_path=None,image_size=(196,196)):
        self.dataset_name=dataset_name
        self.dataset_path=dataset_path
        self.image_size=image_size
        self.dataset_path='../datasets/KDEF/'

    def get_data(self):
        return self._load_KDEF()

    def _load_KDEF(self):
        class_to_arg=get_class_to_arg(self.dataset_name)
        num_classes=len(class_to_arg)

        file_paths=[]
        for folder, subfolders, filenames in os.walk(self.dataset_path):
            for filename in filenames:
                if filename.lower().endswith(('.jpg')):
                    file_paths.append(os.path.join(folder,filename))

        num_faces=len(file_paths)
        y_size, x_size = self.image_size
        faces=np.zeros(shape=(num_faces,y_size,x_size))
        emotions=np.zeros(shape=(num_faces,num_classes))
        for file_arg, file_path in enumerate(file_paths):
            image_array=cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            image_array=cv2.resize(image_array,(y_size,x_size))
            faces[file_arg]=image_array
            file_basename=os.path.basename(file_path)
            file_emotion=file_basename[4:6]
            # there are two file names in the dataset that don't match the given classes
            try:
                emotion_arg=class_to_arg[file_emotion]
            except:
                continue
            emotions[file_arg,emotion_arg]=1
        faces=np.expand_dims(faces,-1)
        return faces, emotions

def get_labels(dataset_name):
    return {0:'AN',1:'DI',2:'AF',3:'HA',4:'SA',5:'SU',6:'NE'}

def get_class_to_arg():
    return {'AN':0,'DI':1,'AF':2,'HA':3,'SA':4,'SU':5,'NE':6}

def split_data(x,y,validation_split=.2):
    num_samples=len(x)
    num_train_samples=int((1-validation_split)*num_samples)
    train_x=x[:num_train_samples]
    train_y=y[:num_train_samples]
    val_x=x[num_train_samples:]
    val_y=y[num_train_samples:]
    train_data=(train_x,train_y)
    val_data=(val_x,val_y)
    return train_data, val_data

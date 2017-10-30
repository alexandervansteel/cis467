import cv2

from keras.models import load_model
from statistics import mode
import numpy as np

from utils.datasets import get_labels
from utils.dataloader import detect_faces
from utils.dataloader import load_detection_model
from utils.dataloader import apply_offsets
from utils.dataloader import draw_text
from utils.preprocessor import preprocess_input

detection_model_path='../trained_models/detection_model/haarcascade_frontalface_default.xml'
emotion_model_path='../trained_models/fer2013_models/fer2013_mini_XCEPTION.117-0.66.hdf5'
emotion_labels=get_labels('fer2013')

# hyper-parameters for bounding boxes shape
frame_window=10
emotion_offsets=(20,40)

# load models
face_detection=load_detection_model(detection_model_path)
emotion_classifier=load_model(emotion_model_path)

# getting input model shapes for inference
emotion_target_size=emotion_classifier.input_shape[1:3]

# window used to calculate probability of current emotion
emotion_window=[]

# start video stream
cv2.namedWindow('window_frame')
video_capture=cv2.VideoCapture(0)
while True:
    bgr_image=video_capture.read()[1]
    gray_image=cv2.cvtColor(bgr_image,cv2.COLOR_BGR2GRAY)
    rgb_image=cv2.cvtColor(bgr_image,cv2.COLOR_BGR2RGB)
    faces=detect_faces(face_detection,gray_image)

    for face_coordinates in faces:
        x1,x2,y1,y2=apply_offsets(face_coordinates,emotion_offsets)
        gray_face=gray_image[y1:y2,x1:x2]
        try:
            gray_face=cv2.resize(gray_face,(emotion_target_size))
        except:
            continue

        gray_face=preprocess_input(gray_face,True)
        gray_face=np.expand_dims(gray_face,0)
        gray_face=np.expand_dims(gray_face,-1)
        emotion_prediction=emotion_classifier.predict(gray_face)
        emotion_probability=np.max(emotion_prediction)
        emotion_label_arg=np.argmax(emotion_prediction)
        emotion_text=emotion_labels[emotion_label_arg]
        emotion_window.append(emotion_text)

        if len(emotion_window)>frame_window:
            emotion_window.pop(0)
        try:
            emotion_mode=mode(emotion_window)
        except:
            continue

        draw_text(face_coordinates,rgb_image,emotion_mode,0,-45,1,1)

    bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
    cv2.imshow('window_frame', bgr_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

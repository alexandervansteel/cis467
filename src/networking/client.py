import queue
from pygame.locals import *
from tkinter import *
from PIL import Image, ImageTk
import socket
import threading
import sys
import os
import signal
sys.path.append('../GUI/')
sys.path.append('../')

BUFF_SIZE = 1500

class Quit(Exception):
    pass


class Killed(Exception):
    pass

def exit_signal(signal, frame):
    raise Quit


def killed_signal(signal, frame):
    raise Killed


def main():
    value = True
    while value:
        server_ip = get_input("IP: ")
        port_num = get_input("Port: ")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server_ip, int(port_num)))
        signal.signal(signal.SIGUSR1, exit_signal)
        signal.signal(signal.SIGUSR2, killed_signal)

        # queues allow communication between main thread and GUI
        # gui_queue sends data from the client to the gui thread
        # client_queue sends data from the gui back to the client
        gui_queue = queue.Queue()
        client_queue = queue.Queue()
        cnn_emo_queue = queue.Queue()
        cnn_img_queue = queue.Queue()

        server = threading.Thread(target=server_handler, args=(s,gui_queue))
        server.daemon = True
        server.start()

        message = threading.Thread(target=message_handler, args=(s,client_queue, cnn_emo_queue))
        message.daemon = True
        message.start()

        cnn =  threading.Thread(target=cnn_handler, args=(cnn_img_queue,cnn_emo_queue))
        cnn.daemon = True
        cnn.start()

        window = Tk()

        messages = Text(window)
        messages.pack()

        input_user = StringVar()
        input_field = Entry(window, text=input_user)
        input_field.pack(side=BOTTOM, fill=X)

        label = Label(window)
        label.pack()

        label2 = Label(window)
        label2.pack()

        def update_msg():
            if gui_queue.empty() == True:
                msg = ""
            else:
                msg = gui_queue.get_nowait()

            if msg[:3] == 'msg':
                messages.insert(INSERT, '%s\n' % msg[3:])

            if msg[:3] == 'lst':
                messages.insert(INSERT, '%s\n' % msg[3:])

            if msg[:3] == 'emo':
                messages.insert(INSERT, '%s\n' % msg[3:])
                im = Image.open('../../emoImages/' + msg[3:] + '.gif')
                tkimage = ImageTk.PhotoImage(im)
                label.image = tkimage 
                label.config(image=tkimage)
                label.pack(side=RIGHT)

            window.after(10, update_msg)

        def show_webcam():
            if cnn_img_queue.empty() == False:
                image = Image.open('emotion.jpg')
                tkimage = ImageTk.PhotoImage(image)
                label2.image = tkimage
                label2.configure(image=tkimage)
                label2.pack()
            
            window.after(10, show_webcam)


        def Enter_pressed(event):
            input_get = input_field.get()
            client_queue.put(input_get)
            # label = Label(window, text=input_get)
            input_user.set('')
            # label.pack()
            return "break"	

        frame = Frame(window)  # , width=300, height=300)
        input_field.bind("<Return>", Enter_pressed)
        frame.pack()

        window.after(10, update_msg)
        show_webcam()
        window.mainloop()


def server_handler(sock,gui_queue):
    while True:
        encodedmsg = sock.recv(BUFF_SIZE)
        msg = encodedmsg.decode('utf-8')
        gui_queue.put(msg)

        if msg[:3] == 'msg':
            print('\n' + msg[3:])
            sys.stdout.flush()
            sys.stdout.write("[]$ ")
            sys.stdout.flush()
            # this output goes to UI to be printed

        if msg[:3] == 'lst':
            print('\n' + msg[3:])
            sys.stdout.flush()
            sys.stdout.write("[]$ ")
            sys.stdout.flush()

        if msg[:3] == 'emo':
            # interface with the UI to display image
            print("emo: " + msg)

        if msg[3:7] == "exit":
            sock.send(("msg" + msg).encode('utf-8'))
            print('\n')
            os.kill(os.getpid(), signal.SIGUSR2)
            return


def message_handler(sock, client_queue, cnn_emo_queue):
    try:
        address = ""
        while True:
            # msg = get_input("[]$ ")
            if client_queue.empty() == False:
                msg = client_queue.get_nowait()
                if msg[:7] == "client=":
                    address = msg[7:13]
                    pass
                else:
                    sock.send(("msg" + address + msg).encode('utf-8'))
                # this output goes to UI to be printed

                if msg[3:7] == "exit" or not msg:
                    os.kill(os.getpid(), signal.SIGUSR1)

            if cnn_emo_queue.empty() == False:
                msg = cnn_emo_queue.get_nowait()
                if address != "":
                    sock.send(("emo" + address + msg).encode('utf-8'))


    except Quit:
        value = False
    except Killed:
        pass
    finally:
        sock.close()


def cnn_handler (cnn_img_queue, cnn_emo_queue):
    import cv2
    import pygame
    import pygame.camera
    from threading import Thread

    from keras.models import load_model
    from statistics import mode
    import numpy as np

    from utils.datasets import get_labels
    from utils.dataloader import detect_faces
    from utils.dataloader import load_detection_model
    from utils.dataloader import apply_offsets
    from utils.dataloader import draw_text
    from utils.preprocessor import preprocess_input

    detection_model_path='../../trained_models/detection_model/haarcascade_frontalface_default.xml'
    emotion_model_path='../../trained_models/KDEF_models/KDEF_mini_XCEPTION.08-0.52.hdf5'
    emotion_labels=get_labels('KDEF')

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

    DEVICE = '/dev/video0'
    SIZE = (640, 480)
    FILENAME = 'capture.png'


    def camstream(display, camera, screen):
        while True:
            screen = camera.get_image(screen)
            display.blit(screen, (0,0))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == QUIT:
                    capture = False
                elif event.type == KEYDOWN and event.key == K_s:
                    pygame.image.save(screen, FILENAME)
        camera.stop()
        pygame.quit()
        return

    pygame.init()
    pygame.camera.init()
    display = pygame.display.set_mode(SIZE, 0)
    camera = pygame.camera.Camera(DEVICE, SIZE)
    camera.start()
    screen = pygame.surface.Surface(SIZE, 0, display)
    bgcam = Thread(target=camstream, args=(display, camera, screen,))
    bgcam.start()


    def getimage(camera, screen):
        scrncap = camera.get_image(screen)
        pygame.image.save(scrncap, 'emotion.jpg')
        image = cv2.imread('emotion.jpg')
        return image


    def getscreen(camera, screen):
        scrncap = camera.get_image(screen)
        return scrncap

    def getemo():
        return emotion_text


    while True:
        bgr_image=getimage(camera, screen)
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

            cnn_emo_queue.put(emotion_text)
            cnn_img_queue.put(getimage(camera, screen))

# def gui_handler(sock, gui_queue, client_queue):
    #import GUI
    # i am going to temporarily avoid importing gui for sprint 2.
    # this means the code is dirty and not modular, will fix.







def get_input(msg):
    sys.stdout.write(msg)
    sys.stdout.flush()
    input = sys.stdin.readline()
    return input

if __name__ == "__main__":
    main()

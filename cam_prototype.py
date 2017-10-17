import numpy as np
import cv2
import pygame
import pygame.camera
from pygame.locals import *
from threading import Thread

DEVICE = '/dev/video0'
SIZE = (640, 480)
FILENAME = 'capture.png'


# opens a camera stream displaying webcam. needed to keep camera 'hot'    
def camstream(display, camera, screen):
    while True:
        screen = camera.get_image(screen)
        display.blit(screen, (0,0))
        pygame.display.flip()
        pygame.image.save(screen, 'test.jpg')
        for event in pygame.event.get():
            if event.type == QUIT:
                capture = False
            elif event.type == KEYDOWN and event.key == K_s:
                pygame.image.save(screen, FILENAME)
    camera.stop()
    pygame.quit()
    return

# function lifts an image from the live webcam and saves, then reloads as
# grayscale with opencv and returns that image. can change to just give file
# name/path if needed for the cnn.
def getimage(camera, screen):
    scrncap = camera.get_image(screen)
    pygame.image.save(scrncap, 'emotion.jpg')
    image = cv2.imread('emotion.jpg')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image

# spawns thread for the webcam stream, camera.get_image is a blocking call
def init():
    pygame.init()
    pygame.camera.init()
    display = pygame.display.set_mode(SIZE, 0)
    camera = pygame.camera.Camera(DEVICE, SIZE)
    camera.start()
    screen = pygame.surface.Surface(SIZE, 0, display)
    bgcam = Thread(target=camstream, args=(display, camera, screen,))
    bgcam.start()
    print("main thread")
    getimage(camera, screen)

if __name__ == "__main__":
    init()

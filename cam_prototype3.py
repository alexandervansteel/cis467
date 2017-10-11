import pygame
import pygame.camera
from pygame.locals import *
from threading import Thread

DEVICE = '/dev/video0'
SIZE = (640, 480)
FILENAME = 'capture.png'

    
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

def getimage(camera, screen):
    scrncap = camera.get_image(screen)
    pygame.image.save(scrncap, 'working.jpg')
    return scrncap

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

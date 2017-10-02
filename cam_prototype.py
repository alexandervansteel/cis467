import numpy as np
import cv2
import time


def takePicture(capture):
    while(True):
        # capture frame-by-frame
        ret, frame = capture.read()

        # our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # display the resulting frame
        im = cv2.imshow('frame', gray)

        # we dont have to write the image if we can pass it directly to the CNN
        cv2.imwrite("test.jpg",gray,[int(cv2.IMWRITE_JPEG_QUALITY),100]) # writes image test.bmp to disk
        print ("image saved")
        if cv2.waitKey(1) & 0xff == ord('q'):
            break
        time.sleep(0.3)

    # returns the image, not the written image jpeg
    return im



def main():
    cap = cv2.VideoCapture(0)
    takePicture(cap)
    # when everything done, release the capture
    cap.release()
    cv2.destroyAllWindows
    return 0


if __name__ == "__main__":main()

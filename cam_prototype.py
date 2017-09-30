import numpy as np
import cv2
cap = cv2.VideoCapture(0)
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    im = cv2.imshow('frame', gray)

    cv2.imwrite("test.jpg",gray,[int(cv2.IMWRITE_JPEG_QUALITY),100]) # writes image test.bmp to disk
    break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()




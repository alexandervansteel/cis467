This should not be integrated as there are still compatibility issues.

For some reason CV2 will not open VideoCapture(0) (the webcam) for reading as it does in Python 2.7. I have narrowed this down to an issue with the ffmpeg library for Python 3, but I cannot find a fix.

Feel free to try to run it on your machines to see if you don't see the same issues as I did.

The error I get is:

OpenCV Error: Assertion failed (scn == 3 || scn == 4) in cvtColor, file /io/opencv/modules/imgproc/src/color.cpp, line 10638
Traceback (most recent call last):
  File "cam_prototype.py", line 38, in <module>
    if __name__ == "__main__":main()
  File "cam_prototype.py", line 31, in main
    takePicture(cap)
  File "cam_prototype.py", line 12, in takePicture
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
cv2.error: /io/opencv/modules/imgproc/src/color.cpp:10638: error: (-215) scn == 3 || scn == 4 in function cvtColor


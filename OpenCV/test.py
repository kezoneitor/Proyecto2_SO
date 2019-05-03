import cv2
import numpy as np
import os
from tkinter import *


try:
    if not os.path.exists('data'):
        os.makedirs('data')
except OSError:
    print ('Error: Creating directory of data')

def change_res(width, height):
    cap.set(3, width)
    cap.set(4, height)

# Playing video from file:
cap = cv2.VideoCapture('test.mp4')
FPS = 30
currentFrame = 0
second = 0
change_res(1920, 1080)
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not (ret):
        break
    else:
        currentFrame += 1
    if (currentFrame%FPS == 0):
        # Saves image of the current frame in jpg file
        name = './data/second_' + str(second) + '.jpg'
        print ('Creating...' + name)
        cv2.imwrite(name, frame)
        second += 1

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
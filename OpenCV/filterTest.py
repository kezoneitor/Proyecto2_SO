import numpy as np
import cv2

cap = cv2.VideoCapture(0)

def change_res(width, height):
    cap.set(3, width)
    cap.set(4, height)

while True:
    ret, frame = cap.read()
    if ret :
        cv2.imshow('frame', frame) #imgshow

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
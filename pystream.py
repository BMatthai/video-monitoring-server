import numpy as np
import cv2


import time
import os


def start_stream():
    os.system("raspivid -o - -t 0 -hf -rot 180 -w 640 -h 480 -fps 24 |cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8554}' :demux=h264")

def shape_detection():
    # multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
    #https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
    fullbody_cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_upperbody.xml')
    eye_cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_eye.xml')
    cap = cv2.VideoCapture(0)
    while 1:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        fullbody = fullbody_cascade.detectMultiScale(gray, 1.3, 5)
        eye = eye_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in fullbody:
            print("Quelque chose qui s'apparente à une silhouette humaine est apparu.")
        for (x,y,w,h) in eye:
            print("Quelque chose qui s'apparente des yeux.")
            # cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            # roi_gray = gray[y:y+h, x:x+w]
            # roi_color = img[y:y+h, x:x+w]
        # cv2.imshow('img',img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()


start_stream()
shape_detection()




import cv2
import io
from picamera import PiCamera
from picamera.array import PiRGBArray
from datetime import datetime
import time

import pickle
import socket
import struct

COOLDOWN_DURATION = 10
HOST=''
PORT=8554

def timestamp_minute():
        """
        This method returns the cur timestamp as minute, in a entire value.
        """
        return int(datetime.timestamp(datetime.now()))

# Tant que 1:
    # Si mouvement:
        # Si non recording:
            # Commencer recording
        # Si recording
            #  D  caller fin recording de X minutes.

def shape_detection():
    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.rotation = 180
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))

    eye_cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_eye.xml')

    isRecording = False
    endRecording = 0

# NEW
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print 'Socket created'

    s.bind((HOST,PORT))
    print 'Socket bind complete'
    s.listen(10)
    print 'Socket now listening'

    conn,addr=s.accept()
# FINNEW

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        data = pickle.dumps(frame)
        clientsocket.sendall(struct.pack("H", len(data))+data)

        img = frame.array

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        eye = eye_cascade.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in eye:
            if (isRecording == False):
                print("Yeux detected, on enregistre")
                camera.start_recording('./recording/VIDEO_' + str(timestamp_minute()) + '.h264')
                isRecording = True
                endRecording = timestamp_minute() + COOLDOWN_DURATION
            else:
                print("Yeux detected on d  cale la fin du recording")
                endRecording = timestamp_minute() + COOLDOWN_DURATION

        if (isRecording == True and timestamp_minute() > endRecording):
            print("Pas vu Dieu depuis 10 seconde, stop recording")
            camera.stop_recording()
            isRecording = False

#                      cv2.imshow('img',img)
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break

        rawCapture.truncate(0)

        cv2.destroyAllWindows()

start_stream()
shape_detection()
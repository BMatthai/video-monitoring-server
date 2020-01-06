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

	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	s.bind((HOST,PORT))
	s.listen(10)

	conn,addr=s.accept()

	encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

	color = (0, 0, 0) 
	thickness = -1
	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		eye = eye_cascade.detectMultiScale(gray, 1.3, 5)
		for (x,y,w,h) in eye:
			frame = cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness) 
			if (isRecording == False):
                camera.start_recording('./recording/VIDEO_' + str(timestamp_minute()) + '.h264')
        		isRecording = True
                endRecording = timestamp_minute() + COOLDOWN_DURATION
			else:
		    	endRecording = timestamp_minute() + COOLDOWN_DURATION

		result, frame = cv2.imencode('.jpg', frame, encode_param)

		data = pickle.dumps(frame, 0)
   		size = len(data)
		# print("{}: {}".format(img_counter, size))
		s.sendall(struct.pack(">L", size) + data)
		# img_counter += 1

shape_detection()

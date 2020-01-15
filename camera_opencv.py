import os
import cv2
from base_camera import BaseCamera
import imutils

from datetime import datetime
import time

import numpy as np
import argparse

from picamera import PiCamera
from picamera.array import PiRGBArray
 
import io

def timestamp_second():
		"""
		This method returns the cur timestamp as minute, in a entire value.
		"""
		return int(datetime.timestamp(datetime.now()))

def available_cooldown(time, cooldown):
	if (timestamp_second() - time > cooldown):
		return True
	return False

def adjust_gamma(image, gamma=1.0):
	# build a lookup table mapping the pixel values [0, 255] to
	# their adjusted gamma values
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")
 
	# apply gamma correction using the lookup table
	return cv2.LUT(image, table)

def detect_cadav(chose_cascade, img, color):
	chose = chose_cascade.detectMultiScale(img, 1.3, 5)
	for (x,y,w,h) in chose:
		print("voiture detected")
		img = cv2.rectangle(img, (x, y), (x + w, y + h), color, 1)
	return img

def transform_image(img):
	# img = cv2.flip(img, -1)
	# img = cv2.blur(img,(5,5))

	img = adjust_gamma(img, gamma=2.5)
	#img = imutils.resize(img, width=640)

	return img

class Camera(BaseCamera):
	video_source = 0

	def __init__(self):
		if os.environ.get('OPENCV_CAMERA_SOURCE'):
			Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
		super(Camera, self).__init__()

	
	@staticmethod
	def set_video_source(source):
		Camera.video_source = source

	@staticmethod
	def frames():

		camera = PiCamera()
		camera.resolution = (640, 480)
		camera.rotation = 180
		camera.framerate = 30

		img = io.BytesIO()


		green_color = (0, 255, 0)
		red_color = (255, 0, 0)

		thickness = 2

		fullbody_cascade = cv2.CascadeClassifier('/home/pi/video-monitoring-server/haarcascades/haarcascade_fullbody.xml')
		cars_cascade = cv2.CascadeClassifier('/home/pi/video-monitoring-server/haarcascades/haarcascade_cars.xml')

		rawCapture=PiRGBArray(camera)
		camera.capture(rawCapture, 'bgr')
		img=rawCapture.array

		img = transform_image(img)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		last_img = img
		last_gray = gray

		last_shape_time = timestamp_second()
		last_move_time = last_shape_time
		start_recording_time = last_shape_time

		recording = False

		# frame_width = int(camera.get(3))
		# frame_height = int(camera.get(4))

		while True:
			img = PiRGBArray(camera)
			camera.capture(img, 'bgr')
			img=rawCapture.array
			# cv2.imwrite('img.jpg',img)

			img = transform_image(img)

			if(recording == True):
				if(available_cooldown(start_recording_time, 10) == False):
					out.write(img)
				else:
					print("Stop recording")
					recording = False
					out.release()

			if (available_cooldown(last_move_time, 0) == True):
				last_move_time = timestamp_second()

				gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
				frameDelta = cv2.absdiff(last_gray, gray)
				thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
				thresh = cv2.dilate(thresh, None, iterations=2)

				cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
				cnts = imutils.grab_contours(cnts)

				for c in cnts:
					longueur_contour = cv2.contourArea(c)
					if (longueur_contour > 300):
						start_recording_time = timestamp_second()
						if (recording == False):
							print("Motion detected start recording : " + str(longueur_contour))
							recording = True
							curDateTime = datetime.now()
							out = cv2.VideoWriter('/home/pi/video-monitoring-server/recording/VIDEO_' + str(longueur_contour) + '|' + str(curDateTime.strftime("%d-%m-%Y_%H:%M:%S")) + '.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 10, (640,480))
						
						if (available_cooldown(last_shape_time, 3) == True):
							last_shape_time = timestamp_second()
							img = detect_cadav(cars_cascade, img, green_color)
							img = detect_cadav(fullbody_cascade, img, red_color)
				last_gray = gray

			yield cv2.imencode('.jpg', img)[1].tobytes()

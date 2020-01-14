import os
import cv2
from base_camera import BaseCamera
import imutils

from datetime import datetime
import time

import numpy as np
import argparse

def timestamp_second():
		"""
		This method returns the cur timestamp as minute, in a entire value.
		"""
		return int(datetime.timestamp(datetime.now()))

def available_cooldown(time):
	if (timestamp_second() - time > 10):
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
		camera = cv2.VideoCapture(Camera.video_source)

		if not camera.isOpened():
			raise RuntimeError('Could not start camera.')

		green_color = (0, 255, 0)
		red_color = (255, 0, 0)
		thickness = 2
		fullbody_cascade = cv2.CascadeClassifier('/home/pi/video-monitoring-server/haarcascades/haarcascade_fullbody.xml')
		cars_cascade = cv2.CascadeClassifier('/home/pi/video-monitoring-server/haarcascades/haarcascade_cars.xml')
		eyes_cascade = cv2.CascadeClassifier('/home/pi/video-monitoring-server/haarcascades/haarcascade_eye.xml')

		_, img = camera.read()

		_, last_img = camera.read()
		# last_img = imutils.resize(last_img, width=500)
		last_img = cv2.flip(last_img, -1)

		last_gray = cv2.cvtColor(last_img, cv2.COLOR_BGR2GRAY)
		last_gray = cv2.GaussianBlur(last_gray, (21, 21), 0)
		
		last_call_time = timestamp_second()
		while True:
			_, img = camera.read()

			# img = imutils.resize(img, width=500)
			img = cv2.flip(img, -1)

			img = adjust_gamma(img, gamma=2.5)
			# img = cv2.GaussianBlur(img, (21, 21), 0)
			# img = cv2.medianBlur(img, 5) 

			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

			frameDelta = cv2.absdiff(last_gray, gray)
			thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
			thresh = cv2.dilate(thresh, None, iterations=2)

			cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
			cnts = imutils.grab_contours(cnts)

			for c in cnts:
				longueur_contour = cv2.contourArea(c)
				if (longueur_contour > 2000):
					print("Motion detected : " + str(longueur_contour))

					if (available_cooldown(last_call_time) == True):
						last_call_time = timestamp_second()
						cars = cars_cascade.detectMultiScale(img, 1.3, 5)
						fullbody = fullbody_cascade.detectMultiScale(img, 1.3, 5)
						for (x,y,w,h) in cars:
							print("voiture detected")
							frameDelta = cv2.rectangle(frameDelta, (x, y), (x + w, y + h), green_color, thickness)
						for (x,y,w,h) in fullbody:
							print("fullbody detected")
							frameDelta = cv2.rectangle(frameDelta, (x, y), (x + w, y + h), red_color, thickness)

			yield cv2.imencode('.jpg', img)[1].tobytes()
			last_gray = gray

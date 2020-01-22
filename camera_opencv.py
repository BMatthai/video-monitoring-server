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

def available_cooldown(time, cooldown):
	if (timestamp_second() - time > cooldown):
		return True
	return False

invGamma = 1.0 / 2.5
table = np.array([((i / 255.0) ** invGamma) * 255
	for i in np.arange(0, 256)]).astype("uint8")

def adjust_gamma(image):
	return cv2.LUT(image, table)

def shape_detection(frame, cascade, color):
	shape = cascade.detectMultiScale(frame, 1.3, 5)
	for (x,y,w,h) in shape:
		frame = cv2.rectangle(frame, (x, y), (x + w, y + h), color, 1)
	return frame

def transform_image(img):
	img = imutils.resize(img, width=500)
	img = adjust_gamma(img)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	return gray

def improve_visibility(img):
	# img = imutils.resize(img, width=640)
	img = cv2.flip(img, -1)
	# img = cv2.blur(img,(5,5))
	img = adjust_gamma(img, gamma=2.5)
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
		camera = cv2.VideoCapture(Camera.video_source)

		if not camera.isOpened():
			raise RuntimeError('Could not start camera.')

		green_color = (0, 255, 0)
		red_color = (255, 0, 0)

		thickness = 2

		fullbody_cascade = cv2.CascadeClassifier('/home/pi/video-monitoring-server/haarcascades/haarcascade_fullbody.xml')
		cars_cascade = cv2.CascadeClassifier('/home/pi/video-monitoring-server/haarcascades/haarcascade_cars.xml')

		_, img = camera.read()
		last_gray = transform_image(img)

		last_shape_time = timestamp_second()
		last_move_time = last_shape_time
		start_recording_time = last_shape_time

		last_longueur_contour = 100000
		recording = False

		frame_width = int(camera.get(3))
		frame_height = int(camera.get(4))

		while True:
			_, img = camera.read()

			if(recording == True):
				if(available_cooldown(start_recording_time, 10) == False):
					out.write(img)
				else:
					print("Stop recording")
					recording = False
					out.release()

			if (available_cooldown(last_move_time, 0) == True):
				last_move_time = timestamp_second()

				gray = transform_image(img)

				frameDelta = cv2.absdiff(last_gray, gray)
				thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
				thresh = cv2.dilate(thresh, None, iterations=2)

				cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
				cnts = imutils.grab_contours(cnts)

				for c in cnts:
					longueur_contour = cv2.contourArea(c)
					
					if (longueur_contour > (2 * last_longueur_contour)):
						start_recording_time = timestamp_second()
						if (recording == False):
							recording = True
							curDateTime = datetime.now()
							out = cv2.VideoWriter('/home/pi/video-monitoring-server/recording/VIDEO_' + str(curDateTime.strftime("%d-%m-%Y_%H:%M:%S")) + '.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
						
						if (available_cooldown(last_shape_time, 3) == True):
							last_shape_time = timestamp_second()
							img = shape_detection(img, cars_cascade, green_color)
							img = shape_detection(img, fullbody_cascade, red_color)
					
					last_longueur_contour = longueur_contour

				last_gray = gray

			img = improve_visibility(img)
			yield cv2.imencode('.jpg', img)[1].tobytes()

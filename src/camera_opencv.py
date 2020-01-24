import os
import cv2
from base_camera import BaseCamera
import imutils

import time

import numpy as np
import argparse

from image_processing import *
from video_recorder import *

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

		ret, frame = camera.read()
		last_gray = transform_image(frame)

		last_shape_time = timestamp_second()
		last_move_time = last_shape_time
		start_recording_time = last_shape_time

		last_longueur_contour = 100000
		recording = False

		while (camera.isOpened()):
			ret, frame = camera.read()

			if(is_recording() == True):
				if(available_cooldown(start_recording_time, 10) == False):
					write_frame(out, frame)
				else:
					stop_recording(out)

			if (available_cooldown(last_move_time, 0) == True):
				last_move_time = timestamp_second()
				gray = transform_image(frame)
				contours = get_contours(last_gray, gray)

				for contour in contours:
					contour_length = cv2.contourArea(contour)
					
					if (contour_threshold_reached(contour_length, last_contour_length) == True):
						start_recording_time = timestamp_second()
						if (is_recording() == False):
							start_recording()
				
						if (available_cooldown(last_shape_time, 3) == True):
							last_shape_time = timestamp_second()
							frame = shape_detection(frame, cars_cascade, green_color)
							frame = shape_detection(frame, fullbody_cascade, red_color)
					
					last_contour_length = contour_length

				last_gray = gray

			frame = improve_visibility(frame)
			yield cv2.imencode('.jpg', frame)[1].tobytes()

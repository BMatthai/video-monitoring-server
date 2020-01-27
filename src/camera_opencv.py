import os
import cv2
from base_camera import BaseCamera
# import imutils

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

		ret, last_frame = camera.read()
		last_gray = to_gray(last_frame)

		while (camera.isOpened()):
			ret, frame = camera.read()

			modified_frame = improve_visibility(frame)
			gray = to_gray(modified_frame)
			entoured_frame = detect_shape(gray)
			detect_motion(gray, last_gray)
			
			yield cv2.imencode('.jpg', entoured_frame)[1].tobytes()
			last_gray = gray
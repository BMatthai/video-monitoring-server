import os
import cv2
from base_camera import BaseCamera

from image_processing import *
from video_recorder import *

import numpy as np
import argparse

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

		if (camera.isOpened() == False): 
			print(STR_ERROR_OPENING_STREAM)

		ret, last_frame = camera.read()
		last_gray = to_gray(last_frame)

		while (camera.isOpened()):
			ret, frame = camera.read()

			if ret == True:
				improved_frame = improve_visibility(frame)
#				improved_frame = frame
				gray = to_gray(improved_frame)

				motion_detected = detect_motion(gray, last_gray)

				if (motion_detected == True):
					# shape_detected, improved_frame = detect_shapes(improved_frame)
					end_record = timestamp_second() + RECORD_SHIFT
					if (VideoRecorder.is_recording == False):
						start_recording()

				if (VideoRecorder.is_recording == True):
					if (outdated(end_record) == False):
						write_frame(improved_frame)
					else:
						stop_recording()

				last_gray = gray

				yield cv2.imencode('.jpg', improved_frame)[1].tobytes()

				if cv2.waitKey(25) & 0xFF == ord('q'):
					break
			else:
				break

		camera.release()
		cv2.destroyAllWindows()

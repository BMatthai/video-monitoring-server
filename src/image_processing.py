import cv2
import numpy as np
from matplotlib import pyplot as plt
from constants import *
import imutils
from time_manager import *
from video_recorder import *

class ImageProcessing:

	def __init__(self):
		self.he_table = np.array([((i / 255.0) ** (1.0 / 2.5)) * 255 for i in np.arange(0, 256)]).astype("uint8")
		self.last_shape_time = TimeManager.timestamp_second()
		self.last_move_time = TimeManager.timestamp_second()
		self.fullbody_cascade = cv2.CascadeClassifier('/home/pi/video-monitoring-server/haarcascades/haarcascade_fullbody.xml')
		self.cars_cascade = cv2.CascadeClassifier('/home/pi/video-monitoring-server/haarcascades/haarcascade_cars.xml')
		self.clahe = cv2.createCLAHE(clipLimit=20.0, tileGridSize=(32,32))

	def detect_shapes(self, frame):
		if (TimeManager.available_cooldown(self.last_shape_time, 1) == True):
			last_shape_time = TimeManager.timestamp_second()
			frame = shape_detection(frame, cars_cascade, GREEN_COLOR)
			frame = shape_detection(frame, fullbody_cascade, RED_COLOR)
			return frame

	def detect_motion(self, gray, last_gray):
		if (TimeManager.available_cooldown(self.last_move_time, 0) == True):
			last_move_time = TimeManager.timestamp_second()
			contours = self.get_contours(gray, last_gray)

			for contour in contours:
				contour_length = cv2.contourArea(contour)
			
				if (self.contour_threshold_reached(contour_length) == True):
					if (VideoRecorder.is_recording() == False):
						VideoRecorder.start_recording()

	def adjust_gamma(self, image):
		return cv2.LUT(image, self.he_table)

	def to_gray(self, img):
		img = imutils.resize(img, width=500)
		img = self.adjust_gamma(img)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (21, 21), 0)

		return gray

	def improve_visibility(self, frame):
		frame = cv2.flip(frame, -1)
		# img = cv2.blur(img,(5,5))
		frame = self.adjust_gamma(frame)
		return frame

	def transform_clahe(image):
		lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
		l, a, b = cv2.split(lab)
		cl = clahe.apply(l)
		limg = cv2.merge((cl, a, b))
		final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
		return final 

	def denoising(frame):
		dst = cv2.fastNlMeansDenoisingColored(frame,None,10,10,7,21)
		return dst

	def denoising_multi(frames):
		dst = cv2.fastNlMeansDenoisingColoredMulti(frames, 2, 5, None, 4, 7, 35)
		return dst

	def shape_detection(frame, cascade, color):
		# TODO Etudier les paramètres 2 et 3 de detectMultiScale
		shape = cascade.detectMultiScale(frame, 1.3, 5)
		for (x,y,w,h) in shape:
			frame = cv2.rectangle(frame, (x, y), (x + w, y + h), color, THICKNESS)
		return frame

	def get_contours(self, gray, last_gray):
		frame_delta = cv2.absdiff(last_gray, gray)
		thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
		thresh = cv2.dilate(thresh, None, iterations=2)

		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		contours = imutils.grab_contours(cnts)

		return contours

	def contour_threshold_reached(self, contour_length):
		return contour_length > CONTOUR_THRESHOLD

# def process_img(frame, last_frame):
# 	# modified_frame = improve_visibility(frame)
# 	# entoured_frame = detect_shape(modified_frame)
# 	# detect_motion(frame, last_frame)

# 	# if(is_recording() == True):
# 	# 	if(available_cooldown(start_recording_time, 10) == False):
# 	# 		write_frame(out, frame)
# 	# 	else:
# 	# 		stop_recording(out)

	

				
		
# 		last_gray = gray

# 	frame = improve_visibility(frame)
# 	return frame
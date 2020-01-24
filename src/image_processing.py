import cv2
import numpy as np
from matplotlib import pyplot as plt

from constants import *

class ImageProcessing:
	
	def __init__(self):
		invGamma = 1.0 / 2.5
		table = np.array([((i / 255.0) ** invGamma) * 255
			for i in np.arange(0, 256)]).astype("uint8")

		self.he_table = table
		self.contour_threshold = 300
		self.clahe = cv2.createCLAHE(clipLimit=20.0, tileGridSize=(32,32))

	def adjust_gamma(image):
		return cv2.LUT(image, he_table)

	def to_gray(img):
		img = imutils.resize(img, width=500)
		img = adjust_gamma(img)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (21, 21), 0)

		return gray

	def improve_visibility(frame):
		frame = cv2.flip(frame, -1)
		# img = cv2.blur(img,(5,5))
		frame = adjust_gamma(frame, gamma=2.5)
		return frame

	def transform_clahe(image):
		lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
		l, a, b = cv2.split(lab)
		cl = self.clahe.apply(l)
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

	def get_contours(last_gray, gray):
		frame_delta = cv2.absdiff(last_gray, gray)
		thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
		thresh = cv2.dilate(thresh, None, iterations=2)

		contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		contours = imutils.grab_contours(cnts)

		return contours

	def contour_threshold_reached(contour_length):
		return contour_length > self.threshold

		# fullbody_cascade = cv2.CascadeClassifier('/home/pi/video-monitoring-server/haarcascades/haarcascade_fullbody.xml')
		# cars_cascade = cv2.CascadeClassifier('/home/pi/video-monitoring-server/haarcascades/haarcascade_cars.xml')

		# last_shape_time = timestamp_second()
		# last_move_time = last_shape_time
		# start_recording_time = last_shape_time

		# recording = False

		# last_gray = transform_image(frame)


	def detect_shapes(frame):
		if (available_cooldown(last_shape_time, 1) == True):
			last_shape_time = timestamp_second()
			frame = shape_detection(frame, cars_cascade, GREEN_COLOR)
			frame = shape_detection(frame, fullbody_cascade, RED_COLOR)
			return frame

	def detect_motion(gray, last_gray):
		if (available_cooldown(last_move_time, 0) == True):
					last_move_time = timestamp_second()
					gray = transform_image(frame)
					contours = get_contours(last_gray, gray)

					for contour in contours:
						contour_length = cv2.contourArea(contour)
					
						if (contour_threshold_reached(contour_length) == True):
							if (is_recording() == False):
								start_recording()

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
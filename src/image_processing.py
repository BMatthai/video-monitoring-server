import numpy as np
import cv2
import imutils
from time_manager import *
from constants import *
from video_recorder import *

# from matplotlib import pyplot as plt

he_table = np.array([((i / 255.0) ** (1.0 / 2.5)) * 255 for i in np.arange(0, 256)]).astype("uint8")
fullbody_cascade = (cv2.CascadeClassifier(PROJECT_PATH + '/haarcascades/haarcascade_fullbody.xml'), "fullbody")
upperbody_cascade = (cv2.CascadeClassifier(PROJECT_PATH + '/haarcascades/haarcascade_upperbody.xml'), "upperbody")
car_cascade = (cv2.CascadeClassifier(PROJECT_PATH + '/haarcascades/haarcascade_car.xml'), "car")
eye_cascade = (cv2.CascadeClassifier(PROJECT_PATH + '/haarcascades/haarcascade_eye.xml'), "eye")
clahe = cv2.createCLAHE(clipLimit=20.0, tileGridSize=(32,32))

def shape_recognition(cascade, shape_name, frame, color):
	shape = cascade.detectMultiScale(frame, 1.2, 5)
	for (x,y,w,h) in shape:
		print(STR_SHAPE_DETECTED + shape_name)
		frame = cv2.rectangle(frame, (x, y), (x + w, y + h), color, THICKNESS)
		take_picture(frame)
	return frame

def detect_shapes(frame):
	if (available_cooldown(TimeManager.last_detect_time, 1) == True):
		TimeManager.last_detect_time = timestamp_second()
		frame = shape_recognition(car_cascade[0], car_cascade[1], frame, GREEN_COLOR)
		frame = shape_recognition(fullbody_cascade[0],fullbody_cascade[1], frame, RED_COLOR)
		frame = shape_recognition(upperbody_cascade[0], upperbody_cascade[1], frame, BLUE_COLOR)
		frame = shape_recognition(eye_cascade[0], eye_cascade[1], frame, YELLOW_COLOR)

	return True, frame

def detect_motion(gray, last_gray):
	if (available_cooldown(TimeManager.last_move_time, 1) == True):
		TimeManager.last_move_time = timestamp_second()
		contours = get_contours(gray, last_gray)

		for contour in contours:
			contour_length = cv2.contourArea(contour)
			if (contour_threshold_reached(contour_length) == True):
				print(STR_MOTION_DETECTED)
				return True
	return False

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
	frame = adjust_gamma(frame)
	return frame

def transform_clahe(image):
	lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
	l, a, b = cv2.split(lab)
	cl = clahe.apply(l)
	limg = cv2.merge((cl, a, b))
	final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
	return final

def get_contours(gray, last_gray):
	frame_delta = cv2.absdiff(last_gray, gray)
	thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
	thresh = cv2.dilate(thresh, None, iterations=2)

	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	contours = imutils.grab_contours(cnts)

	return contours

def contour_threshold_reached(contour_length):
	return contour_length > CONTOUR_THRESHOLD

def denoising(frame):
	dst = cv2.fastNlMeansDenoisingColored(frame, None, 10, 10, 7, 21)
	return dst

def denoising_multi(frames):
	dst = cv2.fastNlMeansDenoisingColoredMulti(frames, 2, 5, None, 4, 7, 35)
	return dst

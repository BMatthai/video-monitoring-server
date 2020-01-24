import cv2
import numpy as np
from matplotlib import pyplot as plt


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
		dst = cv2.fastNlMeansDenoisingColoredMulti(noisy, 2, 5, None, 4, 7, 35)
		return dst

	def shape_detection(frame, cascade, color):
		shape = cascade.detectMultiScale(frame, 1.3, 5)
		for (x,y,w,h) in shape:
			frame = cv2.rectangle(frame, (x, y), (x + w, y + h), color, 1)
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
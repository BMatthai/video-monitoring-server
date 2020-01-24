import cv2
import numpy as np
from matplotlib import pyplot as plt

invGamma = 1.0 / 2.5
table = np.array([((i / 255.0) ** invGamma) * 255
	for i in np.arange(0, 256)]).astype("uint8")

def adjust_gamma(image):
	return cv2.LUT(image, table)

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

clahe = cv2.createCLAHE(clipLimit=20.0, tileGridSize=(32,32))

def transform_clahe(image):
	lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
	l, a, b = cv2.split(lab)
	# clahe = cv2.createCLAHE(clipLimit=20.0, tileGridSize=(20, 20))
	cl = clahe.apply(l)
	limg = cv2.merge((cl, a, b))
	final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
	return final 

def denoising(frame):
	dst = cv2.fastNlMeansDenoisingColored(frame,None,10,10,7,21)
	return dst

def denoising_multi(frames):
	dst = cv2.fastNlMeansDenoisingColoredMulti(noisy, 2, 5, None, 4, 7, 35)
	return dst
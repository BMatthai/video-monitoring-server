import os
import cv2
from base_camera import BaseCamera


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
		thickness = 3
		fullbody_cascade = cv2.CascadeClassifier('/home/pi/video-monitoring-server/haarcascades/haarcascade_fullbody.xml')
		cars_cascade = cv2.CascadeClassifier('/home/pi/video-monitoring-server/haarcascades/haarcascade_cars.xml')
		last_img = None
		while True:
			# read current frame
			_, img = camera.read()
			img = cv2.flip(img, -1)
			
			if (last_img != None and img != None):
				img = imutils.resize(img, width=500)
				gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
				gray = cv2.GaussianBlur(gray, (21, 21), 0)

				last_img = imutils.resize(last_img, width=500)
				last_gray = cv2.cvtColor(last_img, cv2.COLOR_BGR2GRAY)
				last_gray = cv2.GaussianBlur(last_gray, (21, 21), 0)

				frameDelta = cv2.absdiff(last_gray, gray)
				thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

				thresh = cv2.dilate(thresh, None, iterations=2)
				cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
				cv2.CHAIN_APPROX_SIMPLE)
				cnts = imutils.grab_contours(cnts)

				for c in cnts:
					if cv2.contourArea(c) < args["min_area"]:
						continue
					(x, y, w, h) = cv2.boundingRect(c)
					cv2.rectangle(frameDelta, (x, y), (x + w, y + h), (0, 255, 0), 2)
					text = "Occupied"
			# fullbody = fullbody_cascade.detectMultiScale(img, 1.3, 5)
			# cars = cars_cascade.detectMultiScale(img, 1.3, 5)
			# for (x,y,w,h) in fullbody:
			# 	img = cv2.rectangle(img, (x, y), (x + w, y + h), color, thickness)

			# for (x,y,w,h) in cars:
			# 	img = cv2.rectangle(img, (x, y), (x + w, y + h), color, thickness)

			# encode as a jpeg image and return it
			yield cv2.imencode('.jpg', frameDelta)[1].tobytes()
			last_img = img

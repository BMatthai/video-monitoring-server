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
		while True:
			# read current frame
			_, img = camera.read()
			img = cv2.flip(img, -1)
			fullbody = fullbody_cascade.detectMultiScale(img, 1.3, 5)
			cars = cars_cascade.detectMultiScale(img, 1.3, 5)
			for (x,y,w,h) in fullbody:
				img = cv2.rectangle(img, (x, y), (x + w, y + h), color, thickness)

			for (x,y,w,h) in cars:
				img = cv2.rectangle(img, (x, y), (x + w, y + h), color, thickness)

			# encode as a jpeg image and return it
			yield cv2.imencode('.jpg', img)[1].tobytes()

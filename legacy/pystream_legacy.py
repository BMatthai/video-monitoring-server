import cv2
import io
from picamera import PiCamera
from picamera.array import PiRGBArray
from datetime import datetime
import time

import pickle
import socket
import struct

COOLDOWN_DURATION = 10
HOST=''
PORT=8554

app = Flask(__name__)

def timestamp_minute():
		"""
		This method returns the cur timestamp as minute, in a entire value.
		"""
		return int(datetime.timestamp(datetime.now()))

@app.route('/')
def video_feed():
	return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Tant que 1:
	# Si mouvement:
		# Si non recording:
			# Commencer recording
		# Si recording
			#  D  caller fin recording de X minutes.

def gen():
	# initialize the camera and grab a reference to the raw camera capture
	camera = PiCamera()
	camera.resolution = (640, 480)
	camera.rotation = 180
	camera.framerate = 32
	rawCapture = PiRGBArray(camera, size=(640, 480))

	eye_cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_eye.xml')

	isRecording = False
	endRecording = 0

	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	s.bind((HOST,PORT))
	s.listen(10)

	conn,addr=s.accept()

	encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

	color = (0, 0, 0)
	thickness = -1
	img_counter = 0
	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		image = rawCapture.array

		stream.seek(0)
		yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')
		stream.seek(0)
		stream.truncate()
		# image = frame.array
		# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		# eye = eye_cascade.detectMultiScale(gray, 1.3, 5)
		# for (x,y,w,h) in eye:
		# 	image = cv2.rectangle(image, (x, y), (x + w, y + h), color, thickness)
		# 	if (isRecording == False):
		# 		camera.start_recording('./recording/VIDEO_' + str(timestamp_minute()) + '.h264')
		# 		isRecording = True
		# 		endRecording = timestamp_minute() + COOLDOWN_DURATION
		# 	else:
		# 		endRecording = timestamp_minute() + COOLDOWN_DURATION

		# result, image = cv2.imencode('.jpg', image, encode_param)

		# data = pickle.dumps(image, 0)
		# size = len(data)
		# print("{}: {}".format(img_counter, size))
		# yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n')
		# img_counter += 1
		# rawCapture.seek(0)
		# rawCapture.truncate(0)

# shape_detection()
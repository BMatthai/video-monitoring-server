from image_processing import *
import cv2

def read_video():
	camera = cv2.VideoCapture('../sample/video_night.avi')

	if not camera.isOpened():
		raise RuntimeError('Could not start camera.')

	ret, last_frame = camera.read()
	last_gray = to_gray(last_frame)

	while (camera.isOpened()):
		ret, frame = camera.read()

		modified_frame = improve_visibility(frame)
		gray_frame = to_gray(modified_frame)
		entoured_frame = detect_shape(modified_frame)
		detect_motion(gray, last_gray)
		
		yield cv2.imencode('.jpg', entoured_frame)[1].tobytes()
		last_gray = gray

read_video()
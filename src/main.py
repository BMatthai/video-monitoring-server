from image_processing import *
import cv2

def read_video():
	camera = cv2.Videocamerature('../sample/video_night.avi')
	if (camera.isOpened() == False): 
		print("Error opening video stream or file")

	while(camera.isOpened()):
		ret, frame = camera.read()
		if ret == True:
			# cv2.imshow('Frame',frame)
			# cv2.imshow('Frame clahe', transform_clahe(frame))

			if cv2.waitKey(25) & 0xFF == ord('q'):
				break
		else: 
			break

	camera.release() 
	cv2.destroyAllWindows()

read_video()
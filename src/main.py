from image_processing import *
import cv2

def read_video():
	cap = cv2.VideoCapture('../sample/video_night.avi')
	if (cap.isOpened()== False): 
		print("Error opening video stream or file")

	while(cap.isOpened()):
		ret, frame = cap.read()
		if ret == True:
			cv2.imshow('Frame',frame)
			cv2.imshow('Frame clahe', transform_clahe(frame))

			if cv2.waitKey(25) & 0xFF == ord('q'):
				break
		else: 
			break

	cap.release() 
	cv2.destroyAllWindows()

read_video()
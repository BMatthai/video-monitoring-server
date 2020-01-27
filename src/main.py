from image_processing import *
from video_recorder import *
import cv2

# def read_video2():

# 	camera = cv2.VideoCapture('/Users/bmt/Dev/video-monitoring-server/sample/video_night.avi')

# 	if not camera.isOpened():
# 		raise RuntimeError('Could not start camera.')

# 	ret, last_frame = camera.read()
# 	last_gray = to_gray(last_frame)
# 	while True:
# 		ret, frame = camera.read()

# 		# modified_frame = improve_visibility(frame)
# 		# gray_frame = to_gray(modified_frame)
# 		# entoured_frame = detect_shape(modified_frame)
# 		# detect_motion(gray, last_gray)
		
# 		yield cv2.imencode('.jpg', frame)[1].tobytes()
# 		# last_gray = gray
# 		cv2.imshow('Frame', frame)

# 		if cv2.waitKey(25) & 0xFF == ord('q'):
# 			break
# 		else: 
# 			break

# 	cap.release() 
# 	cv2.destroyAllWindows()

def read_video():
	
	imgpro = ImageProcessing()
	videoreco = VideoRecorder()

	camera = cv2.VideoCapture('../sample/video_night.avi')
	if (camera.isOpened() == False): 
		print("Error opening video stream or file")

	ret, last_frame = camera.read()
	last_gray = imgpro.to_gray(last_frame)
	
	while(camera.isOpened()):
		ret, frame = camera.read()
		if ret == True:
			cv2.imshow('Frame',frame)
			
			modified_frame = imgpro.improve_visibility(frame)
			gray = imgpro.to_gray(modified_frame)
			entoured_frame = imgpro.detect_shapes(modified_frame)
			imgpro.detect_motion(gray, last_gray)
			cv2.imshow('Frame clahe', entoured_frame)

			last_gray = gray
			if cv2.waitKey(25) & 0xFF == ord('q'):
				break
		else: 
			break

	cap.release() 
	cv2.destroyAllWindows()


read_video()	

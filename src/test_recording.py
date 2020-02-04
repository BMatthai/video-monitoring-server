from image_processing import *
from video_recorder import *
import cv2

def test_recording():
	camera = cv2.VideoCapture('../sample/video_night.avi')
	# camera = cv2.VideoCapture('../sample/car-detection.mp4')

	if (camera.isOpened() == False): 
		print("Error opening video stream or file")

	ret, last_frame = camera.read()
	last_gray = to_gray(last_frame)

	while (camera.isOpened()):
		ret, frame = camera.read()

		if ret == True:

			# Ameliorer qualité de l'image

			# Montrer l'image
			
			# Recupérer le gray
			# Detecter mouvement
			# Si mouvement:
				# Deplacer time fin de film
				# Si ça filme pas:
					# Commencer à filmer

			# Si ça filme:
			# 	Si time fin de film pas dépassé:
					# Ecrire frame
				# Sinon
					# Stop_filmer

			# Affecter last_gray = gray

			improved_frame = improve_visibility(frame)

			cv2.imshow('Frame', improved_frame)

			gray = to_gray(frame)

			motion_detected = detect_motion(gray, last_gray)

			if (motion_detected == True):
				end_record = timestamp_second() + RECORD_SHIFT
				if (VideoRecorder.is_recording == False):
					start_recording()

			if (VideoRecorder.is_recording == True):
				if (outdated(end_record) == False):
					write_frame(improved_frame)
				else:
					stop_recording()

			last_gray = gray

			if cv2.waitKey(25) & 0xFF == ord('q'):
				break
		else:
			break

	camera.release()

	cv2.destroyAllWindows()

test_recording()



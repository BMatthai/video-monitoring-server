import cv2
from time_manager import *
from constants import *

def start_recording():
	print(STR_START_RECORDING)
	start_recording_time = timestamp_second()
	curDateTime = datetime.now()
	VideoRecorder.is_recording = True

	# Video settings
	video_name = PROJECT_PATH + '/recording/VIDEO_' + formatted_time() + '.avi'
	video_dimension = (FRAME_WIDTH, FRAME_HEIGHT)
	frame_rate = RECORDING_FRAME_RATE
	fourcc = cv2.VideoWriter_fourcc('M','J','P','G')

	VideoRecorder.out = cv2.VideoWriter(video_name, fourcc, frame_rate, video_dimension)

def stop_recording():
	print(STR_END_RECORDING)
	VideoRecorder.is_recording = False
	VideoRecorder.out.release()

def write_frame(frame):
	VideoRecorder.out.write(frame)

def take_picture(frame):
	picture_name = PROJECT_PATH + '/recording/PICTURE_' + formatted_time() + '.jpg'
	cv2.imwrite(picture_name, frame) 

class VideoRecorder:
	is_recording = False
	should_record = False
	out = None
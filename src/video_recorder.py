import cv2
from time_manager import *

frame_width = 640
frame_height = 480

def start_recording():
	print("start recording")
	start_recording_time = timestamp_second()
	curDateTime = datetime.now()
	VideoRecorder.is_recording = True
	out = cv2.VideoWriter('../recording/VIDEO_' + formatted_time() + '.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width, frame_height))
	return out

def stop_recording(out):
	print("stop recording")
	VideoRecorder.is_recording = False
	out.release()

def write_frame(out, frame):
	out.write(frame)

class VideoRecorder:
	is_recording = False
	should_record = False

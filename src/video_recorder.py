import cv2
from time_manager import *

class VideoRecorder:

	recording = False
	start_recording_time = TimeManager.timestamp_second()
	frame_width = 640
	frame_height = 480

	# frame_width = int(camera.get(3))
	# frame_height = int(camera.get(4))

	@staticmethod
	def start_recording():
		start_recording_time = TimeManager.timestamp_second()
		curDateTime = datetime.now()
		recording = True
		out = cv2.VideoWriter('/home/pi/video-monitoring-server/recording/VIDEO_' + TimeManager.formatted_time() + '.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 10, (VideoRecorder.frame_width, VideoRecorder.frame_height))

	@staticmethod
	def stop_recording(out):
		recording = False
		out.release()

	@staticmethod
	def write_frame(out, frame):
		out.write(frame)

	@staticmethod
	def is_recording():
		return VideoRecorder.recording




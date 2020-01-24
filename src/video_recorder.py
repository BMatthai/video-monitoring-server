import cv2

class VideoRecorder:

	def __init__(self):
		self.recording = False
		self.frame_width = 640
		self.frame_height = 480
		# frame_width = int(camera.get(3))
		# frame_height = int(camera.get(4))

	def start_recording():
		curDateTime = datetime.now()
		recording = True
		self.out = cv2.VideoWriter('/home/pi/video-monitoring-server/recording/VIDEO_' + formatted_time() + '.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 10, (self.frame_width, self.frame_height))

	def stop_recording(out):
		recording = False
		out.release()

	def write_frame(out, frame):
		out.write(frame)

	def is_recording():
		return recording




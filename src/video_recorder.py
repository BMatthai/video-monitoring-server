import cv2

recording = False


# frame_width = int(camera.get(3))
# frame_height = int(camera.get(4))

frame_width = 640
frame_height = 480

start_recording(out):
	curDateTime = datetime.now()
	recording = True
	out = cv2.VideoWriter('/home/pi/video-monitoring-server/recording/VIDEO_' + formatted_time() + '.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

stop_recording(out):
	print("Stop recording")
	recording = False
	out.release()

write_frame(out, frame):
	out.write(frame)

is_recording():
	return recording
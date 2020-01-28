from datetime import datetime

def timestamp_second():
	return int(datetime.timestamp(datetime.now()))

def available_cooldown(time, cooldown):
	if (timestamp_second() - time > cooldown):
		return True
	return False

def outdated(time):
	return available_cooldown(time, 0)

def formatted_time():
	curDateTime = datetime.now()
	return str(curDateTime.strftime("%d-%m-%Y_%H:%M:%S"))

class TimeManager:
	last_detect_time = timestamp_second()
	last_move_time = timestamp_second()
	start_recording_time = timestamp_second()
	end_record_time = timestamp_second()
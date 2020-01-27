from datetime import datetime

def timestamp_second():
	return int(datetime.timestamp(datetime.now()))

def available_cooldown(time, cooldown):
	if (timestamp_second() - time > cooldown):
		return True
	return False

def formatted_time():
	curDateTime = datetime.now()
	return str(curDateTime.strftime("%d-%m-%Y_%H:%M:%S"))
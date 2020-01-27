from time_manager import *

time_test = timestamp_second()

def test_cooldown():
	while True:
		if (available_cooldown(time_test, 10)):
			print('ready')
		else:
			print('not ready')


test_cooldown()
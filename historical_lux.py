#!/usr/local/bin/python3


import time
import os


if __name__ == "__main__":
	os.system('touch lux_values.txt')
	for i in range(10):	
		output = os.system('cat /tmp/last_lux_value')
		os.system(f'echo "{time.ctime()} lux_value: {output}" >> lux_values.txt')
		time.sleep(30)
		
# curl -L https://raw.githubusercontent.com/wnminch/verkada/master/historical_lux.py > /mnt/ramdisk/historical_lux.py

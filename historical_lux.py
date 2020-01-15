#!/usr/local/bin/python3


import time
import os


if __name__ == "__main__":
	"""Create text file of lux values overnight"""
	os.system('touch /mnt/ramdisk/lux_values.txt')
	# currently set up to take 16 measurements over the next 8 hours
	for i in range(16):	
		output = os.system('cat /tmp/last_lux_value')
		os.system('echo -e "' + time.ctime() + ' lux_value: ' + str(output) + '\n" >> /mnt/ramdisk/lux_values.txt')
		# wait 30 minutes before next iteration 
		time.sleep(60*30)
		
# curl -L https://raw.githubusercontent.com/wnminch/verkada/master/historical_lux.py > /mnt/ramdisk/historical_lux.py
# python3 /mnt/ramdisk/historical_lux.py >> /dev/null 2>&1

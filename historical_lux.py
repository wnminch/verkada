#!/usr/local/bin/python3

import time
import os


if __name__ == "__main__":
    """Collect Lux values each 30 minutes for 8 hours"""
    os.system('touch /mnt/ramdisk/lux_values.txt')
    for i in range(16):
        with open('/tmp/last_lux_value') as f:
            output = f.read()
        os.system('echo -e "' + time.ctime() + ' lux_value: ' + str(output) + '\n" >> /mnt/ramdisk/lux_values.txt')
        time.sleep(60*30)
		
# curl -L https://raw.githubusercontent.com/wnminch/verkada/master/historical_lux.py > /mnt/ramdisk/historical_lux.py
# python3 /mnt/ramdisk/historical_lux.py >> /dev/null 2>&1
# cat /mnt/ramdisk/lux_values.txt

#!/usr/local/bin/python3

import time
import os

if __name__ == "__main__":
    """Collect ifconfig and route repeatedly"""
    os.system('touch /mnt/ramdisk/nic.txt')

    for i in range(16):
        ifconfig = os.system('ifconfig')
        route = os.system('route')

        os.system('echo -e "' + time.ctime() + '\nNic config: ' + str(ifconfig) + '\n' + str(route) +'\n\n" >> /mnt/ramdisk/nic.txt')
        # time.sleep(60 * 30)

# curl -L https://raw.githubusercontent.com/wnminch/verkada/master/historical_lux.py > /mnt/ramdisk/historical_lux.py
# python3 /mnt/ramdisk/historical_lux.py >> /dev/null
# cat /mnt/ramdisk/lux_values.txt
#!/usr/local/bin/python3

import time
import os

if __name__ == "__main__":
    """Collect ifconfig and route repeatedly"""

    os.system('touch /mnt/ramdisk/nic.txt')

    for i in range(4):
        os.system('echo -e "\n\n' + time.ctime() +'" >> /mnt/ramdisk/nic.txt')
        ifconfig = os.system('ifconfig | grep . >> /mnt/ramdisk/nic.txt')
        route = os.system('route | grep . >> /mnt/ramdisk/nic.txt')
        time.sleep(30)

# curl -L https://raw.githubusercontent.com/wnminch/verkada/master/nic.py > /mnt/ramdisk/nic.py
# python3 /mnt/ramdisk/nic.py >> /dev/null
# cat /mnt/ramdisk/nic.txt

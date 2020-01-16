#!/usr/local/bin/python3

import time
import os

if __name__ == "__main__":
    os.system('touch /mnt/ramdisk/lux_values/txt')
    for i in range(16):
        with open('/tmp/last_lux_value') as f:
            output = f.read()
        os.system('echo -e "' + time.ctime() + ' lux_value: ' + str(output) + '\n" >> /mnt/ramdisk/lux_values.txt')
        time.sleep(5)

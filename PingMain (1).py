#!/usr/local/bin/python3

import time
import os

if __name__ == "__main__":
    """Ping 4 times 2 endpoints every 10 min"""
    os.system('touch /mnt/internal/mmcblk0p7/gwtest.txt')
    os.system('touch /mnt/internal/mmcblk0p7/pingtest.txt')
    os.system('touch /mnt/internal/mmcblk0p7/dnstest.txt')
    i = 0

    while i < 1008:
        os.system("date |  tee -a /mnt/internal/mmcblk0p7/gwtest.txt ;ping -c4 -w10 10.1.10.1 |  tee -a /mnt/internal/mmcblk0p7/gwtest.txt")
        os.system("date |  tee -a /mnt/internal/mmcblk0p7/pingtest.txt ;ping -c4 -w10 8.8.8.8 |  tee -a /mnt/internal/mmcblk0p7/pingtest.txt")
        os.system("date |  tee -a /mnt/internal/mmcblk0p7/dnstest.txt ;ping -c4 -w10 google.com |  tee -a /mnt/internal/mmcblk0p7/dnstest.txt")

        i += 1
        time.sleep(60 * 10)


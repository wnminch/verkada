#!/usr/local/bin/python3

import time
import os


if __name__ == "__main__":
    network_status = "grep 0 /tmp/network_status"
    path = "/mnt/ramdisk/network.txt"
    append = " | tee -a " + path
    os.system("touch " + path)
    os.system("hostname" + append)

    # loop through all the commands each 10 minutes, only iterating if the camera is offline
    while True:
        status = os.system(network_status)
        # status is non-zero if camera is offline
        if True: #status != 0:
            # all commands
            os.system('printf "\n\n=============================================================" >> ' + path)
            os.system("date" + append)
            os.system("cat /tmp/network_status" + append)
            os.system("ifconfig" + append)
            os.system('printf "ping gateway"' + append)
            os.system("route | grep default | awk '{print $2}' | xargs -I{} ping -c 10 {}" + append)
            os.system("route | grep default | awk '{print $2}' | xargs -I{} grep {} /proc/net/arp" + append)
            os.system("grep nameserver /etc/resolv.conf | tail -n 1 | awk '{print $2}' | xargs -I{} ping -c 5 {}" + append)
            os.system("grep nameserver /etc/resolv.conf | tail -n 1 | awk '{print $2}' | xargs -I{} grep {} /proc/net/arp" + append)
            os.system("ping -c 10 8.8.8.8" + append)
            os.system("traceroute -q 3 -n -m 10 8.8.8.8" + append)
            os.system("traceroute -q 3 -n -m 10 api.control.verkada.com" + append)
            # curl tests
            os.system("curl --max-time 10 https://api.control.verkada.com/ping" + append)
            os.system("curl --max-time 10 https://relay.control.verkada.com/ping" + append)
            os.system("curl --max-time 10 https://index.control.verkada.com/ping" + append)
            os.system("curl --max-time 10 https://firmware.control.verkada.com/ping" + append)
            os.system("curl --max-time 10 https://update.control.verkada.com/ping" + append)
            os.system("curl --max-time 10 -vvv https://api.control.verkada.com/ping" + append)

            # DNS
            os.system("grep nameserver /etc/resolv.conf" + append)
            os.system("nslookup api.control.verkada.com" + append)
            os.system("nslookup relay.control.verkada.com" + append)
            os.system("nslookup index.control.verkada.com" + append)
            os.system("nslookup firmware.control.verkada.com" + append)
            os.system("nslookup update.control.verkada.com" + append)
            os.system("nslookup api.control.verkada.com 8.8.8.8")

            os.system("ntpq -p" + append)

            os.system('printf "\n\n=============================================================" >> ' + path)

        time.sleep(60*10)






    """
    
    os.system('touch /mnt/internal/mmcblk0p7/gwtest.txt')
    os.system('touch /mnt/internal/mmcblk0p7/pingtest.txt')
    os.system('touch /mnt/internal/mmcblk0p7/dnstest.txt')
    i = 0

    while i < 1008:
        os.system("date && ping -c4 -w10 192.168.1.1 |  tee -a /mnt/internal/mmcblk0p7/gwtest.txt")
        os.system("date && ping -c4 -w10 8.8.8.8 |  tee -a /mnt/internal/mmcblk0p7/pingtest.txt")
        os.system("date && ping -c4 -w10 google.com |  tee -a /mnt/internal/mmcblk0p7/dnstest.txt")

        i += 1
        time.sleep(60 * 2)
    """
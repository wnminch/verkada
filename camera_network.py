#!/usr/local/bin/python3

import time
import os


if __name__ == "__main__":
    """Upload on camera and run to collect outputs while the camera is offline,
    usage curl -L https://raw.githubusercontent.com/wnminch/verkada/master/camera_network.py > /mnt/ramdisk/camera_network.py
    python3 /mnt/ramdisk/camera_network.py >> /dev/null 2>&1 """

    # Add script analysis of results, IE DNS failure
    # Better location to store results, so they can persist across reloads

    network_status = "grep 0 /tmp/network_status"
    path = "/mnt/ramdisk/network.txt"
    append = " | tee -a " + path
    os.system("touch " + path)
    os.system("hostname" + append)

    # loop through all the commands each 10 minutes, only iterating if the camera is offline
    while True:
        status = os.system(network_status)
        # status is non-zero if camera is offline
        if status != 0:
            # all commands
            os.system('printf "\n\n-------------------------------------------------------------\n" >> ' + path)
            os.system("date" + append)
            os.system('printf "network status: "' + append)
            os.system("cat /tmp/network_status" + append)
            os.system('printf "\nifconfig\n"' + append)
            os.system("ifconfig" + append)

            os.system('printf "\nARP and ping of gateway\n"' + append)
            os.system("route | grep default | awk '{print $2}' | xargs -I{} grep {} /proc/net/arp" + append)
            os.system("route | grep default | awk '{print $2}' | xargs -I{} ping -c 10 {}" + append)
            time.sleep(15)

            os.system('printf "\nARP and ping of DNS server\n"' + append)
            os.system("grep nameserver /etc/resolv.conf | tail -n 1 | awk '{print $2}' | xargs -I{} grep {} /proc/net/arp" + append)
            os.system("grep nameserver /etc/resolv.conf | tail -n 1 | awk '{print $2}' | xargs -I{} ping -c 5 {}" + append)
            time.sleep(15)

            os.system('printf "\nPing google\n"' + append)
            os.system("ping -c 10 8.8.8.8" + append)
            time.sleep(15)
            os.system('printf "\nTraceroute google and api.control.verkada.com\n"' + append)
            os.system("traceroute -q 3 -n -m 10 8.8.8.8" + append)
            time.sleep(15)
            os.system("traceroute -q 3 -n -m 10 api.control.verkada.com" + append)
            time.sleep(15)

            # curl tests
            os.system('printf "\nCurl api, relay, index, firmware, and update endpoints\n"' + append)
            os.system("curl --max-time 10 https://api.control.verkada.com/ping" + append)
            time.sleep(3)
            os.system("curl --max-time 10 https://relay.control.verkada.com/ping" + append)
            time.sleep(3)
            os.system("curl --max-time 10 https://index.control.verkada.com/ping" + append)
            time.sleep(3)
            os.system("curl --max-time 10 https://firmware.control.verkada.com/ping" + append)
            time.sleep(3)
            os.system("curl --max-time 10 https://update.control.verkada.com/ping" + append)
            time.sleep(3)
            os.system('printf "\nVerbose curl of API endpoint\n"' + append)
            os.system("curl --max-time 10 -vvv https://api.control.verkada.com/ping 1>> /mnt/ramdisk/network.txt 2>&1")
            time.sleep(15)

            # DNS
            os.system('printf "\n\nResolv.conf file\n"' + append)
            os.system("grep nameserver /etc/resolv.conf" + append)
            os.system('printf "\nnslookup for api, relay, index, firmware, and update endpoints\n"' + append)
            os.system("nslookup api.control.verkada.com" + append)
            os.system("nslookup relay.control.verkada.com" + append)
            os.system("nslookup index.control.verkada.com" + append)
            os.system("nslookup firmware.control.verkada.com" + append)
            os.system("nslookup update.control.verkada.com" + append)
            os.system('printf "\nnslookup for api endpoint using google\'s DNS server\n"' + append)
            os.system("nslookup api.control.verkada.com 8.8.8.8")

            os.system('printf "\nNTP check\n"' + append)
            os.system("ntpq -p" + append)

            os.system('printf "\n\n-------------------------------------------------------------\n" >> ' + path)

        time.sleep(60*10)

#!/bin/bash
while true; do
printf "\n\n\n--------------------------------------------------------------------------\n" >> Users/verkada/`hostname`_network.txt
date >> Users/verkada/`hostname`_network.txt

printf "\nping 8.8.8.8, gateway, and DNS server\n" >> Users/verkada/`hostname`_network.txt
ping -c 4 8.8.8.8 >> Users/verkada/`hostname`_network.txt
route get default | grep gateway | cut -d' ' -f6- | xargs -I{} ping -c 4 {} >> Users/verkada/`hostname`_network.txt
cat /etc/resolv.conf | grep nameserver | head -1 | cut -d ' ' -f2 | xargs -I{} ping -c 4 {}  >> Users/verkada/`hostname`_network.txt

printf "\npinging local camera and curling lan-server for it\n" >> Users/verkada/`hostname`_network.txt
netstat -n | grep 4100 | head -1 | awk '{print $5}' | cut -d. -f1-4 | xargs -I{} ping -c 4 {} >> Users/verkada/`hostname`_network.txt
netstat -n | grep 4100 | head -1 | awk '{print $5}' | cut -d. -f1-4 | xargs -I{} curl --max-time 10 -k https://{}:4100/ping  1>> Users/verkada/`hostname`_network.txt 2>&1

printf "\nslookup for endpoints, then nslookup using google's DNS server\n" >> Users/verkada/`hostname`_network.txt
nslookup api.control.verkada.com >> Users/verkada/`hostname`_network.txt
nslookup relay.control.verkada.com >> Users/verkada/`hostname`_network.txt
nslookup firmware.control.verkada.com >> Users/verkada/`hostname`_network.txt
nslookup index.control.verkada.com >> Users/verkada/`hostname`_network.txt
nslookup api.control.verkada.com 8.8.8.8  >> Users/verkada/`hostname`_network.txt

printf "\ncurl verkada endpoints\n" >> Users/verkada/`hostname`_network.txt
printf "curl --max-time 10 https://api.control.verkada.com/ping \n" >> Users/verkada/`hostname`_network.txt
curl --max-time 10 https://api.control.verkada.com/ping 1>> Users/verkada/`hostname`_network.txt 2>&1
printf "\ncurl --max-time 10 -k https://13.248.156.50/ping \n" >> Users/verkada/`hostname`_network.txt
curl --max-time 10 -k https://13.248.156.50/ping  1>> Users/verkada/`hostname`_network.txt 2>&1
printf "\ncurl --max-time 10 -k https://76.223.30.163/ping \n" >> Users/verkada/`hostname`_network.txt
curl --max-time 10 -k https://76.223.30.163/ping  1>> Users/verkada/`hostname`_network.txt 2>&1
printf "\ncurl --max-time 10 https://relay.control.verkada.com/ping \n" >> Users/verkada/`hostname`_network.txt
curl --max-time 10 https://relay.control.verkada.com/ping 1>> Users/verkada/`hostname`_network.txt 2>&1
printf "\ncurl --max-time 10 https://firmware.control.verkada.com/ping \n" >> Users/verkada/`hostname`_network.txt
curl --max-time 10 https://firmware.control.verkada.com/ping  1>> Users/verkada/`hostname`_network.txt 2>&1
printf "\ncurl --max-time 10 https://index.control.verkada.com/ping\n" >> Users/verkada/`hostname`_network.txt
curl --max-time 10 https://index.control.verkada.com/ping  1>> Users/verkada/`hostname`_network.txt 2>&1;
sleep 300;
done

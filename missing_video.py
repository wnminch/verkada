#!/usr/local/bin/python3

import requests
import getpass
import json
import re
import sys


def super_user_token(email):
    """Collects the token from the superuser's account"""

    password = getpass.getpass('Password: ')
    otp = input('2fa code: ')
    login_resp = requests.post(
        'https://vprovision.command.verkada.com/user/login',
        json={
            'email': email,
            'password': password,
            'otp': otp
        },
    )
    if login_resp.status_code == 200:
        superuser_token = login_resp.json()['userToken']
        print("INFO: Logging in as superuser")
    else:
        print("ERROR: FAILED TO LOG IN AS SUPERUSER")
        print('status_code: ' + str(login_resp.status_code))
        exit()
    return superuser_token


def missing_files(low_res_zips):
    """Searches the timestamps of the .zip files to find any gaps of footage"""

    temp = ''
    initial_try = True
    new_text = []
    missing_footage = []

    # Only grab low_res zip files, then cut the file name to just the start and end timestamps
    for line in low_res_zips:
        new_text.append(line[-25:-4])

    # sort the text by epoch time
    new_text.sort()

    # compare the end time stamp of the start time stamp of the next entry. If that is missing, note the gap.
    for line in new_text:
        if initial_try:
            temp = line[-10:]
            initial_try = False
            continue
        if temp not in line:
            missing_footage.append(temp + ' to ' + line[:10] + '     ' + str(int(line[:10]) - int(temp)) + ' seconds')
        temp = line[-10:]

    # To protect against false positives
    # make sure the starting time is only seen once, as it should never be seen as an end time
    for entry in missing_footage:
        matches = re.findall(entry[:10], ''.join(low_res_zips))
        if len(matches) > 1: missing_footage.remove(entry)

    # write to file 'missing_footage_list.txt
    with open('missing_footage_list.txt', 'w') as miss_file:
        miss_file.write('Missing Zip Files\nEpoch time:                  Timespan\n')
        for line in missing_footage:
            miss_file.write(line + '\n')


if __name__ == "__main__":
    """Searches camera's zip files to see if there are gaps in the recorded SD footage"""

    if len(sys.argv) < 3:
        print("Usage: ./missing_video.py camera-id email")
        exit(0)

    token = super_user_token(sys.argv[2])
    camera_id = sys.argv[1]
    # python3 missing_video.py 2c952af3-ea92-4ec9-b56c-bf88b9ef2406 william.minch@verkada.com
    command = 'find /mnt/ -iname "*.zip" | grep low_res'
    url = 'https://vproxy.command.verkada.com/_proxy/remotesh/' + camera_id

    with requests.Session() as session:
        x = session.post(url,
                         json={'interpret': command},
                         headers={'X-Verkada-Auth': token})
        data = x.text
    dict_data = json.loads(data)
    zipfiles = dict_data["stdout"]
    zipfiles = zipfiles.split('\n')
    missing_files(zipfiles)

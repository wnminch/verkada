from moviepy.editor import *
import os
import requests
import sys
import getpass


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
        user_token = login_resp.json()['userToken']
        print("INFO: Logging in as superuser")
    else:
        print("ERROR: FAILED TO LOG IN AS SUPERUSER")
        print('status_code: ' + str(login_resp.status_code))
        exit()
    return user_token


if len(sys.argv) < 5:
    print('Usage is /timelapse.py <email> <cameraid> <epoch start time> <epoch end time> <desired video length (sec)>')
    exit(1)

email = sys.argv[1]
camera_from_org = sys.argv[2]
end = sys.argv[4]
start = sys.argv[3]

try:
    desired_duration = int(sys.argv[5])
except ValueError:
    print('Video length should be a number of seconds')
    exit(1)
try:
    if int(end) < int(start):
        print('error in epoch times')
        exit(1)
except ValueError:
    print('error in epoch times')
    exit(1)

# Authenticate to collect token
superuser_token = super_user_token(email)

# Become the user
become_resp = requests.post(
    'https://vprovision.command.verkada.com/user/become',
    json = {'cameraId': camera_from_org},
    headers = {
        'X-Verkada-Auth': superuser_token
    },
)
if become_resp.status_code == 200:
    user_token = become_resp.json()['userToken']
    print("INFO: Became user for camera", camera_from_org)
else:
    print("ERROR: FAILED TO BECOME USER FOR CAMERA ", camera_from_org)
    sys.exit(1)

# Grab the timelapse for the entire time period
# a month is around 900MB, so this doesn't work well for very long time periods

url = 'https://vsubmit.command.verkada.com/library/timelapse.mp4?cameraId=' + camera_from_org + '&end=' + end + '&start=' + start
video = requests.get(url, headers={'X-Verkada-Auth': user_token})

print(video.status_code)

if video.status_code == 200:
    # Write the video to a file
    with open('temp_video.mp4', 'wb') as f:
        f.write(video.content)
    del video
    clip = VideoFileClip('temp_video.mp4')
    time_divisor = clip.duration//desired_duration

    # if the timelapse is shorter than the desired duration, just use original duration
    if time_divisor < 1:
        time_divisor = 1

    clip.fx(vfx.speedx, time_divisor).write_videofile('timelapse_' + camera_from_org + '.mp4', fps=24)
    os.remove('temp_video.mp4')
else:
    print('Failed to get timelapse from command')

#!/bin/python3
import os
import time
import subprocess
import os.path
import boto3


saveDirectory = os.path.join(os.environ.get("SUN_HOME"), "media", os.environ.get("DEPLOYMENT_STAGE"))
res = os.environ.get("SUN-CHASER-RES", "1920x1080")
usb_src = "/dev/video0"
date = time.time()
file = os.path.join(saveDirectory, f'{date}.jpeg')


def capture(**kwargs):
    run_command = f'guvcview --resolution={res} --image={file}  --photo_timer=2 --photo_total=1 -e'
    subprocess.run(args=run_command.split(' '))


def upload(**kwargs):
    if os.path.exists(path=file):
        upload_client = boto3.client('s3')
        with open('filename', 'rb') as data:
            upload_client.client.upload_file(Filename=file,
                                             Bucket=os.environ.get("UPLOAD_BUCKET"),
                                             Key=os.environ.get("DEPLOYMENT_STAGE")+os.path.basename(file))

def main(**kwargs):
    if not os.environ["SUN_HOME"]:
        print('run source environment before running \
               make sure the infra is built out')
    capture()
    upload()


main()

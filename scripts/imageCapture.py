#!/bin/python3
import os
import time
import toml
import subprocess
import os.path
import boto3


saveDirectory = os.path.join(os.environ.get("SUN_HOME"), "media", os.environ.get("DEPLOYMENT_STAGE"))
res = os.environ.get("SUN-CHASER-RES", "1920x1080")
usb_src = "/dev/video0"
date = time.time()
file = os.path.join(saveDirectory, f'{date}.jpeg')


def load_config(configpath = None):
    if configpath is None:
        configpath = os.environ.get('CONFIG-PATH')
    return toml.load(configpath, _dict=dict)



def capture(**kwargs):
    run_command = f'guvcview --resolution={res} --image={file}  --photo_timer=2 --photo_total=1 -e'
    subprocess.run(args=run_command.split(' '))


def upload_s3(**kwargs):
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
    config = load_config()
    capture()
    upload_s3()
    upload_rsync(ip=config['ip'],
                 username=config['username'],
                 password=config['password'])


def upload_rsync(ip: str, username: str, password:str, flags=None, dest_path=file, dest_path_remote=None, **kwargs):
    if flags is None:
        flags = '-arvz'
    if dest_path_remote is None:
        dest_path_remote = os.path.join(f'/home/{username}', file)
    config = load_config()
    run_command = f'export RSYNC_PASSWORD={password}; \
                    rsync {flags} {dest_path} {username}@{ip}:{dest_path_remote}'
    process = subprocess.Popen(command=run_command, stdout=subprocess.PIPE, shell=True)
    if kwargs.get('verbose') is not None:
        proc_stdout = process.communicate()[0].strip()
        print(proc_stdout)


main()

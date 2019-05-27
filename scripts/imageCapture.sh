#!/bin/bash
#short timeLapse script for streamer.
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/bin


# set working directory here
DIR=/home/amar/Pictures/timeLapse
RES=1920x1080
DEV=/dev/video0
DATE=$(date +"%Y-%m-%d_%H%M")
FILE=$DIR/$DATE.jpeg

cd $DIR
#streamer -c $DEV -s $RES -o $FILE -d #use of -d because issues with command output.
guvcview --resolution=$RES --image=$FILE  --photo_timer=2 --photo_total=1 -e

#!/bin/bash

# mount sda1 into /media/Tough/ 
sudo mount /dev/sda1 /media/Tough/
# WD will want this one instead>>
sudo ntfs-3g /dev/sda1 /media/Tough/
sudo chmod 775 /media/Tough
sudo chmod 775 /media/Tough/lapse
# images, no preview, x&y inverted, 1080p, 1h duration, every 3 sec, 4 digits name, saved as jpg
raspistill -bm -hf -vf -w 1920 -h 1080 -t 3600000 -tl 3000 -o /media/Tough/lapse/image%04d.jpg
# unmount sda1
sleep 1m
sudo umount /dev/sda1

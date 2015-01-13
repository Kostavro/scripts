#!/bin/bash

# mount sda1 into /media/Tough/ 
sudo mount /dev/sda1 /media/Tough/
# images, no preview, x&y inverted, 1h duration, every 3 sec, 4 digits name, saved as jpg
raspistill -bm -hf -vf -t 30000 -tl 3000 -o /media/Tough/lapse/image%04d.jpg
# unmount sda1
sudo umount /dev/sda1

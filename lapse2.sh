#!/bin/bash

# Take pictures with raspberry pi camera for timelapse creation
# NOTE: created for personal use, however you may alter it as you please
# Run as SU

# mount disk
flag=true
while $flag; do
read -p "press 1 for WD or press 2 for intenso [1/2]: " choice
if [ $choice == "1" ]
then
	echo "you chose WD"
	ntfs-3g /dev/sda1 /media/Tough
	flag=false
elif [ $choice == "2" ]
then
	echo "you chose intenso"
	mount /dev/sda1 /media/Tough
	flag=false
else
	echo "choose wisely"
fi
done

chmod 775 /media/Tough
chmod 775 /media/Tough/lapse

# resolution
while ! $flag; do
echo -e "choose frame resolution:\n1.720p\n2.1080p\n3.2K"
read res
if [ $res == "1" ]
then
	ww=1280
	hh=720
	flag=false
elif [ $res == "2" ]
then
	ww=1920
	hh=1080
	flag=false
elif [ $res == "3" ]
then
	ww=2560
	hh=1440
	flag=false
else
	echo "choose wisely"
fi
done

# time period
while ! $flag; do
read -p "enter minutes [reminder: 5 hours = 300 minutes]: " period
if [[ $period =~ [0-9] ]]
then
	period=$[period*60000]
	flag=true
else
	echo "choose wisely"
fi
done

# interval
while $flag; do
read -p "enter interval in miliseconds [reminder: 1000ms = 1sec]: " interval 
if [[ $interval =~ [0-9] ]]
then
	flag=false
else
	echo "choose wisely"
fi
done

# take images, no preview, x&y inverted, resolution, period, interval, 4 digits name, saved as jpg
raspistill -bm -hf -vf -w $ww -h $hh -t $period -tl $interval -o /media/Tough/lapse/image%04d.jpg &


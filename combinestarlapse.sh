#!/bin/bash

cp /run/media/kostavro/Tough\ Disc/lapse/000001.jpg /tmp/New
for f in `ls *.jpg`
do
	echo $f
	convert /tmp/New/000001.jpg $f -gravity center -compose lighten -composite -format jpg /tmp/New/000001.jpg
done

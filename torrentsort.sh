#!/bin/bash

# delete unwanted files
find . -type f -name '*.txt' | while read line; do
        title=$line;
        rm -f "$title"
done
find . -type f -name '*.nfo' | while read line; do
        title=$line;
        rm -f "$title"
done
find . -type f -name '*.NFO*' | while read line; do
        title=$line;
        rm -f "$title"
done
find . -type f -name '*.jpg' | while read line; do
        title=$line;
        rm -f "$title"
done
find . -type f -name '*sample*' | while read line; do
        title=$line;
        rm -f "$title"
done
find . -type f -name '*.Sample*' | while read line; do
        title=$line;
        rm -f "$title"
done

# Series
find . -type f -name '*Vikings*' | while read line; do
	title=$line;
	mv -f "$title" ../Vikings/
done

find . -type f -name '*Robot*' | while read line; do
	title=$line;
	mv -f "$title" ../MrRobot/
done

find . -type f -name '*Thrones*' | while read line; do
	title=$line;
	mv -f "$title" ../Game\ of\ Thrones/
done

find . -type f -name '*Westworld*' | while read line; do
	title=$line;
	mv -f "$title" ../Westworld/
done

find . -type f -name '*Korra*' | while read line; do
	title=$line;
	mv -f "$title" ../Avatar/
done

find . -type f -name '*Stranger.Things*' | while read line; do
	title=$line;
	mv -f "$title" ../StrangerThings/
done
find . -type f | grep '[sS][0-9][0-9]' | while read line; do
	title=$line;
	mv -f "$title" ../UnsortedSeries/
done

# hopefully all that's left is movies and their subtitles
find . -type f -name '*.mp4' | while read line; do
	title=$line;
	mv -f "$title" ../MOVIES/
done
find . -type f -name '*.mkv' | while read line; do
	title=$line;
	mv -f "$title" ../MOVIES/
done
find . -type f -name '*.avi' | while read line; do
	title=$line;
	mv -f "$title" ../MOVIES/
done
find . -type f -name '*.srt' | while read line; do
	title=$line;
	mv -f "$title" ../MOVIES/
done

#delete empty directories
find . -type d -empty -delete

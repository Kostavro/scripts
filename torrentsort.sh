#!/bin/bash

find . -type f -name '*S[0-9]{1,2}E[0-9]{1,2}*' | while read line; do
        title=$line;
        if [[ $title =~ Walking ]]; then
        mv "$title" ../WalkingDead/
        elif [[ $title =~ Vikings ]]; then
        mv "$title" ../Vikings/
        elif [[ $title =~ Sherlock ]]; then
        mv "$title" ../Sherlock/
        elif [[ "$title" =~ Homeland ]]; then
        mv "$title" ../Homeland/
        else
        mv "$title" ./UnsortedSeries/
        fi
done


## TO-DO learn how to OR :P

find . -type f -name '*.mp4' | while read line; do
        title=$line;
        mv "$title" ../MOVIES/
done

find . -type f -name '*.srt' | while read line; do
        title=$line;
        mv "$title" ../MOVIES/
done

find . -type f -name '*.avi' | while read line; do
        title=$line;
        mv "$title" ../MOVIES/
done

find . -type f -name '*.mkv' | while read line; do
        title=$line;
        mv "$title" ../MOVIES/
done


#!/bin/bash

while getopts f:t: flag
do
    case "${flag}" in
        f) file=${OPTARG};;
        t) text=${OPTARG};;
    esac
done
echo "File: $file"
echo "Text: $text"
/usr/bin/mplayer -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=${text}&tl=pl" -dumpstream -dumpfile "$file.mp3"

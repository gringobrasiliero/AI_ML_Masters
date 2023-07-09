#!/bin/bash
SECONDS=0
filename='file1.txt'
while read -r number || [ -n "$number" ]
do
	let "number *= 2"
	echo $number >> newfile1.txt
	done < $filename
duration=$SECONDS
echo $duration

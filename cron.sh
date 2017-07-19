#!/bin/bash

# Gets the filename of the file in inputFiles that was first put there, and if it's not blank, call train.py and pass the file path

LATEST_FILENAME=$(ls -ltr ../app/inputFiles | awk '{print $9}' | grep -Ev ^$ | head -1)

if ! [ -z $LATEST_FILENAME ] # if filename not empty 
then
	FILEPATH="inputFile/"$LATEST_FILENAME
	python src/train.py $FILEPATH
	echo "Called train.py on file "$LATEST_FILENAME
else
	echo "There were no files"
fi

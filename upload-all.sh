#!/bin/bash
echo "Start uploading all python files to your micropython device."
for filename in ./src/*.py; do
    ./upload.sh $filename
done
# find src -depth 1 -name "*.py" -exec ./upload.sh {} \;

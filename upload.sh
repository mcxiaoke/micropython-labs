#!/bin/bash
if [ -z "$1" ]; then
    echo -e "\nPlease call '$0 some-file.py' to run this command!\n"
    exit 1
fi
echo "============ Uploading" $1 "============"
./webrepl/webrepl_cli.py -p 123456 "$1" 192.168.1.141:/

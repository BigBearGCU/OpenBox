#!/bin/bash
sudo echo 1 > /proc/acpi/asus/camera
export GCALPYTHONPATH=`pwd`
echo 'setting gcal path to '$GCALPYTHONPATH
export PYTHONPATH=$GCALPYTHONPATH
echo 'setting python path to '$PYTHONPATH

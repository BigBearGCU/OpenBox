#!/bin/bash
export GCALPYTHONPATH=`pwd`
echo 'setting gcal path to '$GCALPYTHONPATH
export PYTHONPATH=${PYTHONPATH}:${GCALPYTHONPATH}
echo 'setting python path to '$PYTHONPATH

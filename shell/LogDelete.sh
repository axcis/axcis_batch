#!/bin/bash -l

export PYTHONPATH="/var/bin/python/axcis_batch/"

date="`date '+%Y-%m-%d'`"
cd /var/bin/python/axcis_batch/src/main/batch/

python3.7 LogDelete.py -date $date -interval 90

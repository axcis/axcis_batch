#!/bin/bash -l

date="`date '+%Y-%m-%d'`"
cd /var/bin/python/axcis_batch/src/main/batch/

python3.7 TimeRecordDelete.py -date $date

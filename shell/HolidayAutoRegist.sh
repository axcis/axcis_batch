#!/bin/bash -l

export PYTHONPATH="/var/bin/python/axcis_batch/"

year="`date '+%Y'`"
cd /var/bin/python/axcis_batch/src/main/batch/

python3.7 HolidayAutoRegist.py -year $year

#!/bin/bash

function _usage()
{
  echo "Usage: $(basename $0) file.rrd data.sqlite"
  exit $@
}

RRD_FILE="$1"
DATA_FILE="$2"

[ -f "$RRD_FILE" ] || _usage 1
[ -f "$DATA_FILE" ] || _usage 1


sqlite3 -separator ' ' "$DATA_FILE" 'SELECT * FROM data' | while read date time kwh1 kwh2 gas
do
  timestamp=$(date -d "$date $time" +"%s")
  rrdupdate "$RRD_FILE" $timestamp:$kwh1:$kwh2:$gas
done

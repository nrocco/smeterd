#!/bin/sh

[ -z "$1" ] && exit 1

rrdtool create "$1" --start 1366750607 --step 300 \
  DS:kwh1:COUNTER:600:0:U \
  DS:kwh2:COUNTER:600:0:U \
  DS:gas:COUNTER:600:0:U \
  RRA:AVERAGE:0.5:1:8640 \
  RRA:AVERAGE:0.5:12:8760 \
  RRA:AVERAGE:0.5:228:3650

echo "rrd file created in $1"

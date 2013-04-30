#!/bin/sh

STEP=3600
PERIOD='--start end-7d --end now'
DIMENSIONS='--width 800 --height 300'

RRD_FILE="$1"
RRD_FILE="test.rrd"
GRAPH_LOC=/var/www/assets.casadirocco.nl/graphs

[ -d $GRAPH_LOC ] || mkdir -p $GRAPH_LOC
[ -f $RRD_FILE ] || exit 1

rrdtool graph $GRAPH_LOC/kwh.png \
  --step $STEP $PERIOD $DIMENSIONS \
  --title 'Energy consumption in kWh' --vertical-label 'kWh' \
  --lower-limit 0 \
  --no-legend \
  DEF:kwh1=$RRD_FILE:kwh1:AVERAGE \
  DEF:kwh2=$RRD_FILE:kwh2:AVERAGE \
  CDEF:kwh1k=kwh1,1000,/ \
  CDEF:kwh2k=kwh2,1000,/ \
  AREA:kwh1k#0000FF:"Average kwh1" \
  AREA:kwh2k#00FF00:"Average kwh2"







rrdtool graph $GRAPH_LOC/gas.png \
  --step $STEP $PERIOD $DIMENSIONS \
  --vertical-label 'Cubic meters' \
  --lower-limit 0 \
  --no-legend \
  DEF:gas=$RRD_FILE:gas:AVERAGE \
  AREA:gas#FF0000:"Average"

echo "<img src=\"kwh.png\" />" > $GRAPH_LOC/index.html
echo "<br/><br/><img src=\"gas.png\" />" >> $GRAPH_LOC/index.html



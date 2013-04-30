#!/bin/sh

sqlite3 -header -column smeter.sqlite "SELECT DATE(date) AS 'Date', \
                                       ((MAX(kwh1)-MIN(kwh1))+(MAX(kwh2)-MIN(kwh2)))*1.0/1000 AS 'Total kWh', \
                                       (MAX(gas)-MIN(gas))*1.0/1000 AS 'Total Gas', \
                                       MAX(kwh1) as 'Meter kWh1', \
                                       MAX(kwh2) as 'Meter kWh2', \
                                       MAX(gas) as 'Meter gas' \
                                       FROM data \
                                       GROUP BY DATE(date)"

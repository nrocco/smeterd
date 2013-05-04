smeterd
=======

Read P1 smart meter packets in Python


installation
------------

It is highly recommended to use virtualenv for this.
After having your virtualenv activated run

    pip install --requirement requirements.txt

This will install the needed python libraries (in this case only pyserial)
which are needed to start reading P1 packets.


usage as a cli application
--------------------------

To get an idea of the available functionality see the `help` output:

    $ bin/smeterd -h


To make `smeterd` output more verbose use the `-v` option on commands.

    $ bin/smeterd -vvv


To get help for a specific subcommand do this:

    $ bin/smeterd {subcommand} -h


Read one packet from your meter using the following command:

    $ bin/smeterd read-meter [--raw]
    Date:       2013-05-04 22:22:32.224929
    kWh 1:      331.557
    kWh 2:      199.339
    Gas:        749.169


If you need to use another serial port then the default `/dev/ttyUSB0` you can
use the above command with the `--serial-port` option:

    $ bin/smeterd read-meter --serial-port /dev/ttyS0


Currently only kwh1, kwh2 and gas usage are read. If you specify the `--raw`
command line option you will see the raw packet from the smart meter.

    $ bin/smeterd read-meter --raw
    /ISk5\2ME382-1004

    0-0:96.1.1(xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx)
    1-0:1.8.1(00331.476*kWh)
    1-0:1.8.2(00199.339*kWh)
    1-0:2.8.1(00000.000*kWh)
    1-0:2.8.2(00000.000*kWh)
    0-0:96.14.0(0001)
    1-0:1.7.0(0000.13*kW)
    1-0:2.7.0(0000.00*kW)
    0-0:17.0.0(0999.00*kW)
    0-0:96.3.10(1)
    0-0:96.13.1()
    0-0:96.13.0()
    0-1:24.1.0(3)
    0-1:96.1.0(xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx)
    0-1:24.3.0(130504210000)(00)(60)(1)(0-1:24.2.1)(m3)
    (00749.123)
    0-1:24.4.0(1)
    !


You can also collect the `kwh1`, `kwh2` and `gas` data into a sqlite database
like this:

    $ bin/smeterd read-meter --database mydata.sqlite


Typically you run this command from `cron` every x minutes (e.g. 5 minutes).


After having collected enough data you can get an overview of your every day
usage by generating a daily usage report like so:

    $ bin/smeterd report --database mydata.sqlite


usage as a python module
------------------------

TODO


usage as a http web service
---------------------------

TODO



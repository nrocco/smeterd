smeterd
=======

Read P1 smart meter packets in Python


installation
------------

It is highly recommended to use virtualenv for this.
After having your virtualenv installed and activated run the following command to install
the `smeterd` package directly from github (using pip)::

    $ pip install https://github.com/nrocco/smeterd/archive/master.zip#egg=smeterd-dev


Alternatively you can manually clone `smeterd` and run setupttools `setup.py`::

    $ git clone https://github.com/nrocco/smeterd.git
    $ cd smeterd
    $ python setup.py install


This will install the needed python libraries (in this case only pyserial)
which are needed to start reading P1 packets.

If you don't want to install `smeterd` as a package you can run it directly
from the root directory of the git repository using the following command but
are responsible for manually installing dependencies::

    $ python -m smeterd


To install the required dependencies manually see `requirements.txt` run::

    $ pip install -r requirements.txt


usage as a cli application
--------------------------

To get an idea of the available functionality see the `help` output::

    $ smeterd -h


To make `smeterd` output more verbose use the `-v` option on any of the
following commands. You can repeat the option to increase verbosity::

    $ smeterd -vvv


To get help for a specific subcommand use the `-h` or `--help` after
having typed the subcommand::

    $ smeterd {subcommand} -h


Read one packet from your meter using the following command::

    $ smeterd read-meter [--raw]
    Date:       2013-05-04 22:22:32.224929
    kWh 1:      331.557
    kWh 2:      199.339
    Gas:        749.169


If you need to use another serial port then the default `/dev/ttyUSB0` you can
use the above command with the `--serial-port` option::

    $ smeterd read-meter --serial-port /dev/ttyS0


Currently only kwh1, kwh2 and gas usage are read. If you specify the `--raw`
command line option you will see the raw packet from the smart meter::

    $ smeterd read-meter --raw
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
like this::

    $ smeterd read-meter --database mydata.sqlite


Typically you run this command from `cron` every x minutes (e.g. 5 minutes)::

    */5 * * * * /path/to/virtualenv/bin/smeterd read-meter -d meter_data.sqlite


After having collected enough data you can get an overview of your every day
usage by generating a daily usage report like so::

    $ smeterd report --database mydata.sqlite

    date         total_kwh   total_gas   kwh1      kwh2       gas     

    2013-04-23   0.176       0.001       300.716   165.041    685.901 
    2013-04-24   4.871       0.813       301.697   168.943    686.714 
    2013-04-25   3.255       0.97        302.716   171.192    687.69


usage as a python module
------------------------

If using `smeterd` as a cli application you will find that its functionality
is quite limited. You can use the `smeterd` package as a regular python module
so you can integrate the reading of P1 packets into your own solutions.

First initiate a new SmartMeter object::

    >>> from smeterd.meter import SmartMeter
    >>> meter = SmartMeter('/dev/ttyS0')


Now to read one packet from the meter::

    >>> packet = meter.read_one_packet()
    >>> print packet

Do not forget to close the connection to the serial port::

    >>> meter.disconnect()


The `SmartMeter.meter.read_one_packet()` function will return an instance of
the `smeterd.meter.P1Packet` class.

Currently `7` values are extracted from the raw P1 packets::

    packet.date
    packet.uid
    packet.kwh1
    packet.kwh2
    packet.gas
    packet.tariff
    packet.current_usage


usage as a http web service
---------------------------

TODO

smeterd
=======

![Continious Integration](https://github.com/nrocco/smeterd/workflows/Continious%20Integration/badge.svg?branch=master)

Read P1 smart meter packets in Python


installation
------------

`smeterd` is fully python 3.6+ compatible.

It is highly recommended to use virtualenv for this.
After having your virtualenv installed and activated run the following command to install
the `smeterd` package directly from pypi (using pip):

    $ pip install smeterd


Alternatively you can manually clone `smeterd` and run setupttools `setup.py`:

    $ git clone https://github.com/nrocco/smeterd.git
    $ cd smeterd
    $ python setup.py install


This will install the needed python libraries (in this case only pyserial)
which are needed to start reading P1 packets.

If you don't want to install `smeterd` as a package you can run it directly
from the root directory of the git repository using the following command but
you are responsible for manually installing dependencies:

    $ python -m smeterd



usage as a cli application
--------------------------

To get an idea of the available functionality see the `help` output:

    $ smeterd -h


To make `smeterd` output more verbose use the `-v` option on any of the
following commands. You can repeat the option to increase verbosity:

    $ smeterd -vvv


To get help for a specific subcommand use the `-h` or `--help` after
having typed the subcommand:

    $ smeterd {subcommand} -h


Read one packet from your meter using the following command:

    $ smeterd read-meter
    Time                      2013-08-25 10:10:45.337563
    Total kWh High consumed   651038
    Total kWh Low consumed    546115
    Total gas consumed        963498
    Current kWh tariff        1
    Gas Measured At           1516562094


By default the `read-meter` commands spits out the current date, total kwh1,
total kwh2, total gas amounts and current kWh tariff on multiple lines.

You can make it print the same values as a tab seperated list:

    $ smeterd read-meter --tsv
    2013-05-04 22:22:32.224929	331557	199339	749169	1	1516562094


By piping the output of the `read-meter --tsv` command to a bash script you can fully
customize what you want to do with the data:

    IFS='{tab}'
    while read date kwh1 kwh2 gas tariff gas_measured_at; do
      mysql my_database -e "INSERT INTO data VALUES ('$date', $kwh1, $kwh2, $gas, $tariff, $gas_measured_at);"
    done < /dev/stdin


Typically you run this command from `cron` every x minutes (e.g. 5 minutes):

    */5 * * * * /path/to/venv/bin/smeterd read-meter | save_to_mysql_script.sh


If you need to use another serial port then the default `/dev/ttyUSB0` you can
use the above command with the `--serial-port` option:

    $ smeterd read-meter --serial-port /dev/ttyS0


Currently only kwh1, kwh2 and gas usage are read. If you specify the `--raw`
command line option you will see the raw packet from the smart meter:

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




usage as a python module
------------------------

If using `smeterd` as a cli application you will find that its functionality
is quite limited. You can use the `smeterd` package as a regular python module
so you can integrate the reading of P1 packets into your own solutions.

First initiate a new SmartMeter object:

    >>> from smeterd.meter import SmartMeter
    >>> meter = SmartMeter('/dev/ttyS0')


Now to read one packet from the meter:

    >>> packet = meter.read_one_packet()
    >>> print packet

Do not forget to close the connection to the serial port:

    >>> meter.disconnect()


The `SmartMeter.meter.read_one_packet()` function will return an instance of
the `smeterd.meter.P1Packet` class.


contribute
----------

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Make sure that tests pass (`make test`)
5. Push to the branch (`git push origin my-new-feature`)
6. Create new Pull Request

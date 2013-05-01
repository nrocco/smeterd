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


usage
-----

Read one packet from your meter using the following command:

    ./meter-read-once.py [sqlite.database]

The first argument is optional but if you give a valid path to a sqlite
database it will write the data to this database instead of stdout.
Currently only kwh1, kwh2 and gas usage are read and stored.


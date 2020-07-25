NORMAL_PACKET = b'''/ISk5\2ME382-1004\r
\r
0-0:96.1.1(XXXXXXXXXXXXXXMYSERIALXXXXXXXXXXXXXX)\r
1-0:1.8.1(00608.400*kWh)\r
1-0:1.8.2(00490.342*kWh)\r
1-0:2.8.1(00000.001*kWh)\r
1-0:2.8.2(00000.000*kWh)\r
0-0:96.14.0(0001)\r
1-0:1.7.0(0001.51*kW)\r
1-0:2.7.0(0000.00*kW)\r
0-0:17.0.0(0999.00*kW)\r
0-0:96.3.10(1)\r
0-0:96.13.1()\r
0-0:96.13.0()\r
0-1:24.1.0(3)\r
0-1:96.1.0(3238303131303031323332313337343132)\r
0-1:24.3.0(130810180000)(00)(60)(1)(0-1:24.2.1)(m3)\r
(00947.680)\r
0-1:24.4.0(1)\r
!\r
'''

NORMAL_PACKET_1003 = b'''/ISk5\2ME382-1003\r
\r
0-0:96.1.1(5A424556303035303933313937373132)\r
1-0:1.8.1(00608.400*kWh)\r
1-0:1.8.2(00490.342*kWh)\r
1-0:2.8.1(00000.001*kWh)\r
1-0:2.8.2(00000.000*kWh)\r
0-0:96.14.0(0001)\r
1-0:1.7.0(0001.51*kW)\r
1-0:2.7.0(0000.00*kW)\r
0-0:17.0.0(0999.00*kW)\r
0-0:96.3.10(1)\r
0-0:96.13.1()\r
0-0:96.13.0()\r
!\r
'''

BROKEN_PACKET = b'''1-0:1.7.0(0001.51*kW)\r
1-0:2.7.0(0000.00*kW)\r
0-0:17.0.0(0999.00*kW)\r
0-0:96.3.10(1)\r
0-0:96.13.1()\r
0-0:96.13.0()\r
0-1:24.1.0(3)\r
0-1:96.1.0(3238303131303031323332313337343132)\r
0-1:24.3.0(130810180000)(00)(60)(1)(0-1:24.2.1)(m3)\r
(00947.680)\r
0-1:24.4.0(1)\r
!\r
'''

LONG_BROKEN_PACKET = b'''/ISk5\2ME382-1004\r
\r
0-0:96.1.1(XXXXXXXXXXXXXXMYSERIALXXXXXXXXXXXXXX)\r
1-0:1.8.1(00608.400*kWh)\r
1-0:1.8.2(00490.342*kWh)\r
1-0:2.8.1(00000.001*kWh)\r
1-0:2.8.2(00000.000*kWh)\r
0-0:96.14.0(0001)\r
1-0:1.7.0(0001.51*kW)\r
1-0:2.7.0(0000.00*kW)\r
0-0:17.0.0(0999.00*kW)\r
0-0:96.3.10(1)\r
0-0:96.13.1()\r
0-0:96.13.0()\r
0-1:24.1.0(3)\r
0-1:96.1.0(3238303131303031323332313337343132)\r
0-1:24.3.0(130810180000)(00)(60)(1)(0-1:24.2.1)(m3)\r
(00947.680)\r
0-1:24.4.0(1)\r
\r
/ISk5\2ME382-1004\r
\r
0-0:96.1.1(XXXXXXXXXXXXXXMYSERIALXXXXXXXXXXXXXX)\r
1-0:1.8.1(00608.400*kWh)\r
1-0:1.8.2(00490.342*kWh)\r
1-0:2.8.1(00000.001*kWh)\r
1-0:2.8.2(00000.000*kWh)\r
0-0:96.14.0(0001)\r
1-0:1.7.0(0001.51*kW)\r
1-0:2.7.0(0000.00*kW)\r
0-0:17.0.0(0999.00*kW)\r
0-0:96.3.10(1)\r
0-0:96.13.1()\r
0-0:96.13.0()\r
0-1:24.1.0(3)\r
0-1:96.1.0(3238303131303031323332313337343132)\r
0-1:24.3.0(130810180000)(00)(60)(1)(0-1:24.2.1)(m3)\r
(00947.680)\r
0-1:24.4.0(1)\r
\r
/ISk5\2ME382-1004\r
\r
0-0:96.1.1(XXXXXXXXXXXXXXMYSERIALXXXXXXXXXXXXXX)\r
1-0:1.8.1(00608.400*kWh)\r
1-0:1.8.2(00490.342*kWh)\r
1-0:2.8.1(00000.001*kWh)\r
1-0:2.8.2(00000.000*kWh)\r
0-0:96.14.0(0001)\r
1-0:1.7.0(0001.51*kW)\r
1-0:2.7.0(0000.00*kW)\r
0-0:17.0.0(0999.00*kW)\r
0-0:96.3.10(1)\r
0-0:96.13.1()\r
0-0:96.13.0()\r
0-1:24.1.0(3)\r
0-1:96.1.0(3238303131303031323332313337343132)\r
0-1:24.3.0(130810180000)(00)(60)(1)(0-1:24.2.1)(m3)\r
(00947.680)\r
0-1:24.4.0(1)\r
'''

NORMAL_PACKET_KAIFA1 = b'''/KFM5KAIFA-METER\r
\r
1-3:0.2.8(42)\r
0-0:1.0.0(160905191440S)\r
0-0:96.1.1(XXXXXXXXXXXXXXMYSERIALXXXXXXXXXXXXXX)\r
1-0:1.8.1(000498.215*kWh)\r
1-0:1.8.2(000550.159*kWh)\r
1-0:2.8.1(000000.001*kWh)\r
1-0:2.8.2(000000.000*kWh)\r
0-0:96.14.0(0002)\r
1-0:1.7.0(00.235*kW)\r
1-0:2.7.0(00.000*kW)\r
0-0:96.7.21(00008)\r
0-0:96.7.9(00003)\r
1-0:99.97.0(1)(0-0:96.7.19)(000101000015W)(2147483647*s)\r
1-0:32.32.0(00000)\r
1-0:52.32.0(00000)\r
1-0:72.32.0(00000)\r
1-0:32.36.0(00000)\r
1-0:52.36.0(00000)\r
1-0:72.36.0(00000)\r
0-0:96.13.1()\r
0-0:96.13.0()\r
1-0:31.7.0(000*A)\r
1-0:51.7.0(000*A)\r
1-0:71.7.0(000*A)\r
1-0:21.7.0(00.086*kW)\r
1-0:41.7.0(00.122*kW)\r
1-0:61.7.0(00.027*kW)\r
1-0:22.7.0(00.000*kW)\r
1-0:42.7.0(00.000*kW)\r
1-0:62.7.0(00.000*kW)\r
0-1:24.1.0(003)\r
0-1:96.1.0(4730303235303033333337343136333136)\r
0-1:24.2.1(160905190000S)(00323.528*m3)\r
!189D\r
'''

NORMAL_PACKET_KAIFA2 = b'''/XMX5LGBBFFB231158062\r
\r
1-3:0.2.8(42)\r
0-0:1.0.0(160904220447S)\r
0-0:96.1.1(XXXXXXXXSERIALXXXXXXXXXXX)\r
1-0:1.8.1(004018.859*kWh)\r
1-0:2.8.1(000000.002*kWh)\r
1-0:1.8.2(002827.154*kWh)\r
1-0:2.8.2(000000.000*kWh)\r
0-0:96.14.0(0001)\r
1-0:1.7.0(00.341*kW)\r
1-0:2.7.0(00.000*kW)\r
1-0:32.36.0(00000)\r
0-0:96.13.1()\r
0-0:96.13.0()\r
1-0:31.7.0(002*A)\r
1-0:21.7.0(00.341*kW)\r
1-0:22.7.0(00.000*kW)\r
0-1:24.1.0(003)\r
0-1:96.1.0(4730303233353631323139373231393134)\r
0-1:24.2.1(160904220000S)(05290.211*m3)\r
!F31D\r
'''

NORMAL_PACKET_KAIFA3 = b'''/KFM5KAIFA-METER\r
\r
1-3:0.2.8(42)\r
0-0:1.0.0(161106184601W)\r
0-0:96.1.1(XXXXXXXXSERIALXXXXXXXXXXX)\r
1-0:1.8.1(000608.303*kWh)\r
1-0:1.8.2(000598.271*kWh)\r
1-0:2.8.1(000000.000*kWh)\r
1-0:2.8.2(000000.000*kWh)\r
0-0:96.14.0(0001)\r
1-0:1.7.0(01.263*kW)\r
1-0:2.7.0(00.000*kW)\r
0-0:96.7.21(00001)\r
0-0:96.7.9(00001)\r
1-0:99.97.0(1)(0-0:96.7.19)(000101000001W)(2147483647*s)\r
1-0:32.32.0(00000)\r
1-0:32.36.0(00000)\r
0-0:96.13.1()\r
0-0:96.13.0()\r
1-0:31.7.0(005*A)\r
1-0:21.7.0(01.263*kW)\r
1-0:22.7.0(00.000*kW)\r
0-1:24.1.0(003)\r
0-1:96.1.0(4730303332353631323639323539363136)\r
0-1:24.2.1(161106180000W)(00230.576*m3)\r
!1C29\r
'''

NORMAL_PACKET_CRC_VALID = b'''/KFM5KAIFA-METER\r
\r
1-3:0.2.8(42)\r
0-0:1.0.0(161107095940W)\r
0-0:96.1.1(xxxxxxxxxxxx7777777777777777xxxxxx)\r
1-0:1.8.1(001875.155*kWh)\r
1-0:1.8.2(001890.280*kWh)\r
1-0:2.8.1(000000.000*kWh)\r
1-0:2.8.2(000000.000*kWh)\r
0-0:96.14.0(0002)\r
1-0:1.7.0(00.080*kW)\r
1-0:2.7.0(00.000*kW)\r
0-0:96.7.21(00005)\r
0-0:96.7.9(00003)\r
1-0:99.97.0(1)(0-0:96.7.19)(000101000001W)(2147483647*s)\r
1-0:32.32.0(00000)\r
1-0:32.36.0(00000)\r
0-0:96.13.1()\r
0-0:96.13.0()\r
1-0:31.7.0(000*A)\r
1-0:21.7.0(00.080*kW)\r
1-0:22.7.0(00.000*kW)\r
0-1:24.1.0(003)\r
0-1:96.1.0(473203320330232333343373930338794)\r
0-1:24.2.1(161107090000W)(01350.170*m3)\r
!68AD\r
'''

NORMAL_PACKET_CRC_INVALID = b'''/KFM5KAIFA-METER\r
\r
1-3:0.2.8(42)\r
0-0:1.0.0(161107095940W)\r
0-0:96.1.1(xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx)\r
1-0:1.8.1(001875.155*kWh)\r
1-0:1.8.2(001890.280*kWh)\r
1-0:2.8.1(000000.000*kWh)\r
1-0:2.8.2(000000.000*kWh)\r
0-0:96.14.0(0002)\r
1-0:1.7.0(00.080*kW)\r
1-0:2.7.0(00.000*kW)\r
0-0:96.7.21(00005)\r
0-0:96.7.9(00003)\r
1-0:99.97.0(1)(0-0:96.7.19)(000101000001W)(2147483647*s)\r
1-0:32.32.0(00000)\r
1-0:32.36.0(00000)\r
0-0:96.13.1()\r
0-0:96.13.0()\r
1-0:31.7.0(000*A)\r
1-0:21.7.0(00.080*kW)\r
1-0:22.7.0(00.000*kW)\r
0-1:24.1.0(003)\r
0-1:96.1.0(473203320330232333343373930338794)\r
0-1:24.2.1(161107090000W)(01350.170*m3)\r
!656A\r
'''

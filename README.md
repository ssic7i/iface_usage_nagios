# iface_usage_nagios plugin
Dependency: vnstat

params:

-i - interface

-t - time for checking in seconds

-rx - limitations for input trafic

-tx - limitations for output trafic

for limitations warning and critical edge sepatated by comma. ex: 10,20

example:

iface_usage.py -i eth0 -t 3 -rx 10,20 -tx 10,20
